import io
import json
import os
import time

import requests
from PIL import Image, ImageOps

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


class MTGCardData(CardData):

    json_folder = os.path.join("download", "mtg", "json")
    art_folder = os.path.join("download", "mtg", "art")
    image_folder = os.path.join("download", "mtg", "card")

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
        print(name)
        self.card_image = None

        try:
            faces = self.response_json["card_faces"]

            try:
                art = self.get_artwork(self.name, self.response_json["image_uris"]["art_crop"])
            except KeyError:
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
            except KeyError:
                pass

        return SimpleCardData(face_json["name"], top_right, face_json["type_line"], face_json["oracle_text"], "", bottom_right, image)

    def get_artwork(self, name, image_uri) -> Image:
        if self.artworks[name] is None:
            art_path = self.to_filename(self.art_folder, "png")
            if os.path.isfile(art_path):
                self.artworks[name] = Image.open(art_path)
            else:
                img_data = requests.get(image_uri).content
                self.artworks[name] = Image.open(io.BytesIO(img_data))
                self.artworks[name] = ImageOps.grayscale(self.artworks[name])
                new_height = int(self.IMAGE_WIDTH / self.artworks[name].width * self.artworks[name].height)
                self.artworks[name] = self.artworks[name].resize((self.IMAGE_WIDTH, new_height))

                if not os.path.isdir(self.art_folder):
                    os.makedirs(self.art_folder)
                self.artworks[name].save(art_path)
                time.sleep(0.1)

        return self.artworks[name]

    def get_card_image(self) -> Image:
        if self.card_image is None:
            image_path = self.to_filename(self.image_folder, "png")
            if os.path.isfile(image_path):
                self.card_image = Image.open(image_path)
            else:
                try:
                    uri = self.response_json["image_uris"]["png"]
                except KeyError:
                    uri = self.response_json["card_faces"][0]["image_uris"]["png"]

                img_data = requests.get(uri).content
                self.card_image = Image.open(io.BytesIO(img_data))

                if not os.path.isdir(self.image_folder):
                    os.makedirs(self.image_folder)
                self.card_image.save(image_path)
                time.sleep(0.1)

        return self.card_image


    def to_filename(self, folder, extension):
        return os.path.join(folder, self.name.replace("//", "&&") + "." + extension)

    def print_self(self, printer, postfix="\n\n\n\n"):
        # Double-sided and split card printing
        for card_data in self.card_data_components[:-1]:
            card_data.print_self(printer, postfix="\n")
            printer.set(align="center")
            printer.text("-" * 20 + "\n")
        self.card_data_components[-1].print_self(printer, postfix=postfix)



if __name__ == "__main__":
    ire_shaman = MTGCardData("Ire shaman")
    ire_shaman.get_artwork().show()
    ire_shaman.get_card_image().show()
