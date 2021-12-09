import io
import os
import pickle
from typing import List

import pokemontcgsdk
import requests
from PIL import Image, ImageOps, ImageEnhance

from daemons.PrinterDaemon import PrinterDaemon, printer
from data.SimpleCardData import SimpleCardData
from dotenv import load_dotenv

load_dotenv()
pokemontcgsdk.RestClient.configure(os.getenv("POKEMON_API_KEY"))


def print_card_from_name(print_queue, name):
    card = PokemonCardData(*name.split(" "))
    card.queue_print(print_queue)


TYPE_SYMBOL_DICT = {"Colorless": "{CL}",
                    "Darkness": "{DK}",
                    "Dragon": "{DG}",
                    "Fairy": "{FY}",
                    "Fighting": "{FT}",
                    "Fire": "{FR}",
                    "Grass": "{GR}",
                    "Lightning": "{LT}",
                    "Metal": "{MT}",
                    "Psychic": "{PS}",
                    "Water": "{WA}"}


def cost_to_str(cost: List[str]) -> str:
    return "".join(map(lambda x: TYPE_SYMBOL_DICT[x], cost))


def modifier_to_str(modifier) -> str:
    return "{} {}".format(TYPE_SYMBOL_DICT[modifier.type], modifier.value)


class PokemonCardData(SimpleCardData):

    data_folder = os.path.join("download", "pokemon", "data")
    art_folder = os.path.join("download", "pokemon", "art")

    def __init__(self, set_code: str, card_num: str, art=True):
        # Get saved data, or get new data from the api
        self.set_code = set_code
        self.card_num = card_num
        pickle_path = self.to_filename(self.data_folder, "pkl")
        if os.path.isfile(pickle_path):
            with open(pickle_path, "rb") as f:
                card_data = pickle.load(f)
        else:
            card_data = pokemontcgsdk.Card.where(q='set.ptcgoCode:{} number:{}'.format(set_code, card_num))[0]
            if not os.path.isdir(self.data_folder):
                os.makedirs(self.data_folder)
            with open(pickle_path, "wb") as f:
                pickle.dump(card_data, f)

        self.card_data = card_data

        self.name = card_data.name
        typeline = "{} - {}".format(card_data.supertype, " ".join(card_data.subtypes))
        body = "\n".join([] if card_data.rules is None else card_data.rules)
        top_right = ""
        bottom_left = ""
        bottom_center = ""
        bottom_right = ""

        if card_data.supertype == "Pokémon":
            top_right = "{}, {} HP".format(" ".join(card_data.types), card_data.hp)
            if card_data.evolvesFrom:
                # Avoid unnessecary newline
                if body != "":
                    body = "Evolves from {}\n{}".format(card_data.evolvesFrom, body)
                else:
                    body = "Evolves from " + card_data.evolvesFrom
            # start keeping a trailing newline
            if body == "":
                body = "\n"

            if card_data.ancientTrait:
                body += "{}: {}\n".format(card_data.ancientTrait.name, card_data.ancientTrait.text)
            if card_data.abilities:
                for ability in card_data.abilities:
                    body += "{}: {}\n{}\n".format(ability.type, ability.name, ability.text)
            if card_data.attacks:
                for attack in card_data.attacks:
                    if attack.text == "":
                        body += "{} {}     {}\n".format(cost_to_str(attack.cost), attack.name, attack.damage)
                    else:
                        body += "{} {}     {}\n{}\n".format(cost_to_str(attack.cost), attack.name, attack.damage,
                                                            attack.text)
            if card_data.weaknesses:
                bottom_left = "; ".join(map(modifier_to_str, card_data.weaknesses))
            if card_data.resistances:
                bottom_center = "; ".join(map(modifier_to_str, card_data.resistances))
            bottom_right = "Retreat: " + cost_to_str(card_data.retreatCost)

        self.artwork = None
        if art:
            self.get_artwork(card_data.images.small)
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
                art = art.crop((19, 34, 206, 128))

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
        return self.card_data.images.large

    def to_filename(self, folder, extension, name=None):
        if name is None:
            name = "{}_{}".format(self.set_code, self.card_num)
        return os.path.join(folder, name.replace("//", "&&") + "." + extension)


BASIC_ENERGY = {"Grass Energy":     PokemonCardData("XY", "132", False),
                "Fire Energy":      PokemonCardData("XY", "133", False),
                "Water Energy":     PokemonCardData("XY", "134", False),
                "Lightning Energy": PokemonCardData("XY", "135", False),
                "Psychic Energy":   PokemonCardData("XY", "136", False),
                "Fighting Energy":  PokemonCardData("XY", "137", False),
                "Darkness Energy":  PokemonCardData("XY", "138", False),
                "Metal Energy":     PokemonCardData("XY", "139", False),
                "Fairy Energy":     PokemonCardData("XY", "140", False)}

if __name__ == "__main__":
    print(os.getenv("POKEMON_API_KEY"))
    pd = PrinterDaemon()
    # p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x3)
    hewwo = PokemonCardData("XY", "141")
    print(hewwo.raw_print)
    printer._raw(hewwo.raw_print)
    pd.print_queue.put(hewwo.raw_print)
    pd.run()
