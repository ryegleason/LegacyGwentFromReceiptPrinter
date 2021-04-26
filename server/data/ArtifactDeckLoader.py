import io
import os
from pathlib import Path
from typing import List

import util
from data.ArtifactCardData import ArtifactCardData
from data.ArtifactDeckDecoder import MyArtifactDeckDecoder
from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from data.MTGCardData import MTGCardData
from data.FiniteDeckManager import FiniteDeckManager
from proto.protobuf import reqrep_pb2


class ArtifactDeckLoader(DeckLoader):

    def __init__(self, deck_codes_file):
        decoder = MyArtifactDeckDecoder()
        self.decks = {}
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
        cards = deck["cards"]
        items = []

        for card in cards:
            new_card = ArtifactCardData(card[0])
            print(card)

        for hero in heroes:
            print(hero)

        # cards = []
        # uuids = []
        # image_uris = []
        # image_indices = []
        # image_index = 0
        #
        # copies = int(line.split(" ")[0])
        # # Split and double sided card handling
        # name = line[line.index(" "):].replace("/", " // ").strip()
        #
        # card_data = MTGCardData(name)
        # image_uris.append(card_data.get_card_image_uri())
        #
        # for i in range(copies):
        #     new_card = Card(card_data)
        #     cards.append(new_card)
        #     new_uuid = reqrep_pb2.UUID()
        #     util.UUID_to_proto_UUID(new_card.uuid, new_uuid)
        #     uuids.append(new_uuid)
        #
        #     image_indices.append(image_index)
        #
        # image_index += 1
        #
        # manager = FiniteDeckManager(cards)
        # response = manager.setup()
        # response.new_cards.card_uuids.extend(uuids)
        # response.new_cards.image_uris.extend(image_uris)
        # response.new_cards.image_indices.extend(image_indices)
        # return manager, response


if __name__ == "__main__":
    loader = ArtifactDeckLoader(r"G:\Documents\MixedProjects\LegacyGwentFromReceiptPrinter\server\decks\artifact_decks.txt")
    print(loader.get_deck_names())
    loader.load_deck(loader.get_deck_names()[0])
