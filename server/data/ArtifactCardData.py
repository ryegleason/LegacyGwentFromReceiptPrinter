import io
import json
import os
import re
import time

import requests
from PIL import Image, ImageOps, ImageEnhance
from escpos.printer import Usb

from data.CardData import CardData
from data.SimpleCardData import SimpleCardData

html_remover = re.compile("[<].*?[>]")

LANG = "english"

with open("data/artifact_set_0.json", "r", encoding="utf-8") as f:
    set_0 = json.load(f)["card_set"]["card_list"]

with open("data/artifact_set_1.json", "r", encoding="utf-8") as f:
    set_1 = json.load(f)["card_set"]["card_list"]

id_to_card_dict = {}

for card in set_0:
    if card["card_type"] in ["Hero", "Creep", "Improvement", "Spell", "Item"]:
        id_to_card_dict[card["card_id"]] = card

for card in set_1:
    if card["card_type"] in ["Hero", "Creep", "Improvement", "Spell", "Item"]:
        id_to_card_dict[card["card_id"]] = card


class ArtifactCardData(SimpleCardData):
    IMAGE_WIDTH = 300

    art_folder = os.path.join("download", "artifact", "art")

    def __init__(self, card_id):
        self.card_id = card_id
        data = id_to_card_dict[card_id]
        self.data = data
        self.type = data["card_type"]
        self.name = data["card_name"][LANG]
        crosslane = data.get("is_crosslane", False)
        top_right = str(data.get("mana_cost", ""))
        if crosslane:
            top_right = "<" + top_right + ">"
        typeline = ""
        if data.get("is_red", False):
            typeline += "Red "
        if data.get("is_blue", False):
            typeline += "Blue "
        if data.get("is_green", False):
            typeline += "Green "
        if data.get("is_black", False):
            typeline += "Black "

        typeline += self.type

        subtype = data.get("sub_type")
        if subtype is not None:
            typeline += " - " + subtype

        body = data.get("card_text").get(LANG, "")
        body = body.replace("<br/>", "\n")
        html_remover.sub("", body)
        bottom_left = str(data.get("attack", ""))
        bottom_center = str(data.get("armor", ""))
        if self.is_item():
            bottom_right = data.get("gold_cost", "")
        else:
            bottom_right = data.get("hit_points", "")

        self.artwork = None
        self.get_artwork(data["mini_image"]["default"])

        self.includes = []
        for ref in data.get("references", []):
            if ref.get("ref_type") == "includes":
                self.includes.append([ref["card_id"], ref["count"]])
        super().__init__(self.name, top_right, typeline, body, bottom_left, str(bottom_right), self.artwork,
                         bottom_center=bottom_center)

    def get_artwork(self, image_uri) -> Image:
        if self.artwork is None:
            art_path = self.to_filename(self.art_folder, "png", name=self.name)
            if os.path.isfile(art_path):
                self.artwork = Image.open(art_path)
            else:
                img_data = requests.get(image_uri).content
                art = Image.open(io.BytesIO(img_data))

                enhancer = ImageEnhance.Contrast(art)
                art = enhancer.enhance(2)
                art = ImageOps.grayscale(art)
                art = art.point(lambda x: 255 - (255 - x)/2)

                if not os.path.isdir(self.art_folder):
                    os.makedirs(self.art_folder)
                art.save(art_path)
                self.artwork = art

        return self.artwork

    def get_card_image_uri(self) -> str:
        return self.data["large_image"]["default"]

    def is_item(self) -> bool:
        return self.type == "Item"

    def to_filename(self, folder, extension, name=None):
        if name is None:
            name = self.name
        return os.path.join(folder, name.replace("/", "&") + "." + extension)


if __name__ == "__main__":
    p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)
    hewwo = ArtifactCardData(10148)
    p._raw(hewwo.raw_print)
