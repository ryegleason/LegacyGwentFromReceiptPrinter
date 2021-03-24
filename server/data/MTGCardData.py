import io
import json
import os
import time

import requests
from PIL import Image, ImageOps

from data.CardData import CardData

time_of_last_scryfall_call = 0


def request_from_scryfall(req) -> requests.Response:
    global time_of_last_scryfall_call
    time_since_last = time.time() - time_of_last_scryfall_call
    if time_since_last < 0.1:
        time.sleep(0.1 - time_since_last)
    time_of_last_scryfall_call = time.time()
    return requests.get(req)


class MTGCardData(CardData):

    art_folder = os.path.join("download", "mtg", "art")
    image_folder = os.path.join("download", "mtg", "card")

    def __init__(self, name):
        self.response_json = json.loads(request_from_scryfall("https://api.scryfall.com/cards/named?exact=" +
                                                              name.replace(" ", "+")).content)

        super().__init__(self.response_json["name"], self.response_json["mana_cost"], self.response_json["type_line"],
                         self.response_json["oracle_text"], "",
                         self.response_json["power"] + "/" + self.response_json["toughness"])

    def get_artwork(self) -> Image:
        if self.artwork is None:
            art_path = os.path.join(self.art_folder, self.name.replace("//", "&&") + ".png")
            if os.path.isfile(art_path):
                self.artwork = Image.open(art_path)
            else:
                img_data = requests.get(self.response_json["image_uris"]["art_crop"]).content
                self.artwork = Image.open(io.BytesIO(img_data))
                self.artwork = ImageOps.grayscale(self.artwork)
                new_height = int(self.IMAGE_WIDTH / self.artwork.width * self.artwork.height)
                self.artwork = self.artwork.resize((self.IMAGE_WIDTH, new_height))

                if not os.path.isdir(self.art_folder):
                    os.makedirs(self.art_folder)
                self.artwork.save(art_path)
                time.sleep(0.1)

        return self.artwork

    def get_card_image(self) -> Image:
        if self.card_image is None:
            image_path = os.path.join(self.image_folder, self.name.replace("//", "&&") + ".png")
            if os.path.isfile(image_path):
                self.card_image = Image.open(image_path)
            else:
                img_data = requests.get(self.response_json["image_uris"]["png"]).content
                self.card_image = Image.open(io.BytesIO(img_data))

                if not os.path.isdir(self.image_folder):
                    os.makedirs(self.image_folder)
                self.card_image.save(image_path)
                time.sleep(0.1)

        return self.card_image


if __name__ == "__main__":
    ire_shaman = MTGCardData("Ire shaman")
    ire_shaman.get_artwork().show()
    ire_shaman.get_card_image().show()
