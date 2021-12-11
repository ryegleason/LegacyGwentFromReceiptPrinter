import io
import json
import os
import time

import requests
from PIL import Image, ImageOps, ImageEnhance
from escpos.printer import Usb

from daemons.PrinterDaemon import PrinterDaemon, printer
from data.CardData import CardData
from data.SimpleCardData import SimpleCardData

time_of_last_scryfall_call = 0


def request_from_scryfall(req) -> requests.Response:
    global time_of_last_scryfall_call
    time_since_last = time.time() - time_of_last_scryfall_call
    if time_since_last < 0.1:
        time.sleep(0.1 - time_since_last)
    time_of_last_scryfall_call = time.time()
    return requests.get(req)


def print_card_from_name(print_queue, name):
    card = MTGCardData(name)
    card.queue_print(print_queue)


class MTGCardData(CardData):
    IMAGE_WIDTH = 300

    json_folder = os.path.join("download", "mtg", "json")
    art_folder = os.path.join("download", "mtg", "art")

    def __init__(self, name):
        # Get saved json, or get new json from scryfall
        self.name = name
        json_path = self.to_filename(self.json_folder, "json")
        if os.path.isfile(json_path):
            with open(json_path, "r") as f:
                self.response_json = json.load(f)
        else:
            self.response_json = json.loads(request_from_scryfall("https://api.scryfall.com/cards/named?exact=" +
                                                                  name.replace(" ", "+")).content)
            if not os.path.isdir(self.json_folder):
                os.makedirs(self.json_folder)
            with open(json_path, "w") as f:
                json.dump(self.response_json, f)

        self.card_data_components = []
        self.artworks = {}

        self.name = self.response_json["name"]
        self.card_image = None

        try:
            faces = self.response_json["card_faces"]

            try:
                art = self.get_artwork(self.name, self.response_json["image_uris"]["art_crop"])
            except KeyError as e:
                # Different art for each face
                art = None

            for face in faces:
                self.card_data_components.append(self.build_simple_card_data(face, art))
        except KeyError:
            self.card_data_components.append(self.build_simple_card_data(self.response_json, None))

        super().__init__()

    def build_simple_card_data(self, face_json, image=None):
        # Non creatures don't have a P/T
        try:
            bottom_right = face_json["power"] + "/" + face_json["toughness"]
        except KeyError:
            bottom_right = ""

        # Lands don't have a mana cost
        try:
            top_right = face_json["mana_cost"]
        except KeyError:
            top_right = ""

        # Fetch image if there is one
        if image is None:
            try:
                image = self.get_artwork(face_json["name"], face_json["image_uris"]["art_crop"])
            except KeyError as e:
                pass

        return SimpleCardData(face_json["name"], top_right, face_json["type_line"].replace("—", "-"), face_json["oracle_text"], "", bottom_right, image)

    def get_artwork(self, name, image_uri) -> Image:
        if name not in self.artworks or self.artworks[name] is None:
            art_path = self.to_filename(self.art_folder, "png", name=name)
            if os.path.isfile(art_path):
                self.artworks[name] = Image.open(art_path)
            else:
                img_data = requests.get(image_uri).content
                art = Image.open(io.BytesIO(img_data))
                new_height = int(self.IMAGE_WIDTH / art.width * art.height)

                enhancer = ImageEnhance.Contrast(art)
                art = enhancer.enhance(2)

                art = art.resize((self.IMAGE_WIDTH, new_height))
                art = ImageOps.grayscale(art)
                art = art.point(lambda x: 255 - int((255 - x)/2))

                if not os.path.isdir(self.art_folder):
                    os.makedirs(self.art_folder)
                art.save(art_path)
                self.artworks[name] = art

        return self.artworks[name]

    def get_card_image_uri(self) -> str:
        try:
            uri = self.response_json["image_uris"]["png"]
        except KeyError:
            uri = self.response_json["card_faces"][0]["image_uris"]["png"]
        return uri

    def to_filename(self, folder, extension, name=None):
        if name is None:
            name = self.name
        return os.path.join(folder, name.replace("//", "&&") + "." + extension)

    def print_self(self, printer, postfix="\n\n\n\n"):
        # Double-sided and split card printing
        for card_data in self.card_data_components[:-1]:
            card_data.print_self(printer, postfix="\n")
            printer.set(align="center")
            printer.text("-" * 20 + "\n")
        self.card_data_components[-1].print_self(printer, postfix=postfix)


if __name__ == "__main__":
    pd = PrinterDaemon()
    # p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)
    hewwo = MTGCardData("Fireball")
    print(hewwo.raw_print)
    # printer._raw(hewwo.raw_print)
    pd.print_queue.put(hewwo.raw_print)
    pd.print_queue.put(MTGCardData("Goblin").raw_print)
    pd.run()
