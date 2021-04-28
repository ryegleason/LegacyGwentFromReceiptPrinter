import io
import os
from pathlib import Path
from typing import List

from escpos.printer import Dummy

import util
from data.ArtifactCardData import ArtifactCardData
from data.ArtifactDeckDecoder import MyArtifactDeckDecoder
from data.ArtifactDeckManager import ArtifactDeckManager
from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from data.MTGCardData import MTGCardData
from data.FiniteDeckManager import FiniteDeckManager
from proto.protobuf import reqrep_pb2


class ArtifactDeckLoader(DeckLoader):

    def __init__(self, deck_codes_file, printer):
        decoder = MyArtifactDeckDecoder()
        self.decks = {}
        self.printer = printer
        if os.path.isfile(deck_codes_file):
            with open(deck_codes_file, "r") as f:
                for line in f:
                    if line.strip() != "":
                        deck = decoder.ParseDeck(line.strip())
                        self.decks[deck["name"]] = deck

    def get_deck_names(self) -> List[str]:
        return list(self.decks.keys())

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        deck = self.decks[name]
        heroes = deck["heroes"]
        other = deck["cards"]

        hero_card_data = [None] * 2
        main_deck_cards = []
        item_deck_cards = []

        for card in other:
            new_card = ArtifactCardData(card[0])
            if new_card.is_item():
                item_deck_cards.append((new_card, card[1]))
            else:
                main_deck_cards.append((new_card, card[1]))

        for hero in heroes:
            hero_card = ArtifactCardData(hero[0])
            if hero[1] == 1:
                hero_card_data.insert(0, hero_card)
            else:
                # 3 -> -1, 2 -> -2
                hero_card_data[(-4 + hero[1])] = hero_card

            for include in hero_card.includes:
                item_deck_cards.append((ArtifactCardData(include[0]), include[1]))

        uuids = []
        deck_cards = []
        item_cards = []
        image_uris = []
        image_indices = []
        image_index = 0

        for (card_data, copies) in main_deck_cards:
            image_uris.append(card_data.get_card_image_uri())

            for i in range(copies):
                new_card = Card(card_data)
                deck_cards.append(new_card)
                new_uuid = reqrep_pb2.UUID()
                util.UUID_to_proto_UUID(new_card.uuid, new_uuid)
                uuids.append(new_uuid)

                image_indices.append(image_index)

            image_index += 1

        for (card_data, copies) in item_deck_cards:
            for i in range(copies):
                item_cards.append(Card(card_data))

        manager = ArtifactDeckManager(deck_cards, hero_card_data, item_cards)
        manager.set_printer(self.printer)
        response = manager.setup()
        response.new_cards.card_uuids.extend(uuids)
        response.new_cards.image_uris.extend(image_uris)
        response.new_cards.image_indices.extend(image_indices)
        return manager, response


if __name__ == "__main__":
    loader = ArtifactDeckLoader(r"G:\Documents\MixedProjects\LegacyGwentFromReceiptPrinter\server\decks\artifact_decks.txt", Dummy())
    print(loader.get_deck_names())
    loader.load_deck(loader.get_deck_names()[0])
