import io
import json
import os
import time

import requests
from PIL import Image, ImageOps, ImageEnhance

from data.SimpleCardData import SimpleCardData

time_of_last_ygopro_call = 0

def request_from_ygopro(req) -> requests.Response:
    global time_of_last_ygopro_call
    time_since_last = time.time() - time_of_last_ygopro_call
    if time_since_last < 0.1:
        time.sleep(0.1 - time_since_last)
    time_of_last_ygopro_call = time.time()
    return requests.get(req)


def print_card_from_name(print_queue, name):
    card = YGOCardData.from_name(name)
    card.queue_print(print_queue)

class YGOCardData(SimpleCardData):
    IMAGE_WIDTH = 300

    json_folder = os.path.join("download", "ygo", "json")
    card_art_folder = os.path.join("download", "ygo", "art")
    card_images_folder = os.path.join("static", "images", "ygo")

    def __init__(self, response_json):
        self.response_json = response_json
        self.name = self.response_json["name"]
        self.id = self.response_json["id"]

        json_path = os.path.join(self.json_folder, str(self.id) + ".json")
        if not os.path.isfile(json_path):
            if not os.path.isdir(self.json_folder):
                os.makedirs(self.json_folder)
            with open(json_path, "w") as f:
                json.dump(self.response_json, f)

        # if "race" in response_json:
        #     typeline = "{} - {}".format(response_json["type"], response_json["race"])
        # else:
        #     typeline = response_json["type"]
        body = response_json.get("desc", "")
        typeline = ""
        top_right = ""
        bottom_right = ""

        if "scale" in response_json:
            body = "Pendulum: " + str(response_json["scale"]) + "\n" + body
        if "linkval" in response_json:
            body += "\nLink directions: " + ", ".join(response_json["linkmarkers"])

        if "Monster" in response_json["type"] or response_json["type"] == "Token":
            if "level" in response_json:
                top_right = "Level {} ".format(response_json["level"])
            top_right += response_json["attribute"]

            if "linkval" in response_json:
                bottom_right = "ATK/{} LINK-{}".format(response_json["atk"], response_json["linkval"])
            else:
                bottom_right = "ATK/{} DEF/{}".format(response_json["atk"], response_json["def"])

            types = [response_json["race"]]
            for type_word in response_json["type"].split(" "):
                if type_word not in ["Monster", "Effect", "Normal"]:
                    types.append(type_word)
            if not ("Normal" in response_json["type"] or response_json["type"] == "Ritual Monster" or response_json["type"] == "Token"):
                types.append("Effect")

            typeline = "[" + " - ".join(types) + "]"
        else:
            top_right = response_json["type"]
            if response_json["race"] != "Normal":
                top_right += " - " + response_json["race"]

        self.card_image_uri = "/static/images/ygo/{}.jpg".format(self.id)
        self.get_artwork(response_json["card_images"][0]["image_url_cropped"])


        super().__init__(self.name, top_right, typeline, body, "", bottom_right=bottom_right, artwork=self.artwork)

    @classmethod
    def from_name(cls, name):
        response_json = json.loads(request_from_ygopro("https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" +
                                                             name).content)
        return cls(response_json["data"][0])

    def get_artwork(self, image_uri) -> Image:
        art_path = os.path.join(self.card_art_folder, str(self.id) + ".png")
        if os.path.isfile(art_path):
            self.artwork = Image.open(art_path)
        else:
            img_data = requests.get(image_uri).content
            art = Image.open(io.BytesIO(img_data))
            new_height = int(self.IMAGE_WIDTH / art.width * art.height)

            enhancer = ImageEnhance.Contrast(art)
            art = enhancer.enhance(2)

            art = art.resize((self.IMAGE_WIDTH, new_height))
            art = ImageOps.grayscale(art)
            art = art.point(lambda x: 255 - int((255 - x)/2))

            if not os.path.isdir(self.card_art_folder):
                os.makedirs(self.card_art_folder)
            art.save(art_path)
            self.artwork = art

        image_path = os.path.join(self.card_images_folder, str(self.id) + ".jpg")
        if not os.path.isfile(image_path):
            full_image_data = requests.get(self.response_json["card_images"][0]["image_url"]).content
            full_image = Image.open(io.BytesIO(full_image_data))

            if not os.path.isdir(self.card_images_folder):
                os.makedirs(self.card_images_folder)
            full_image.save(image_path)

        return self.artwork

    def get_card_image_uri(self) -> str:
        return self.card_image_uri
