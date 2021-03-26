import io
import os
from pathlib import Path
from typing import List

import util
from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from data.MTGCardData import MTGCardData
from data.FiniteDeckManager import FiniteDeckManager
from proto.protobuf import reqrep_pb2


class MTGDeckLoader(DeckLoader):

    def __init__(self, deck_dir):
        self.deck_dir = deck_dir
        self.deck_names = []
        if os.path.isdir(deck_dir):
            for deck_filename in Path(deck_dir).rglob("*.txt"):
                self.deck_names.append(deck_filename.with_suffix('').name)

    def get_deck_names(self) -> List[str]:
        return self.deck_names

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        cards = []
        uuids = []
        image_uris = []
        image_indices = []
        image_index = 0

        with open(os.path.join(self.deck_dir, name + ".txt"), "r") as f:
            for line in f:
                if line.strip() == "":
                    break
                copies = int(line.split(" ")[0])
                # Split and double sided card handling
                name = line[line.index(" "):].replace("/", " // ").strip()

                card_data = MTGCardData(name)
                image_uris.append(card_data.get_card_image_uri())

                for i in range(copies):
                    new_card = Card(card_data)
                    cards.append(new_card)
                    new_uuid = reqrep_pb2.UUID()
                    util.UUID_to_proto_UUID(new_card.uuid, new_uuid)
                    uuids.append(new_uuid)

                    image_indices.append(image_index)

                image_index += 1

        manager = FiniteDeckManager(cards)
        response = manager.setup()
        response.new_cards.card_uuids.extend(uuids)
        response.new_cards.image_uris.extend(image_uris)
        response.new_cards.image_indices.extend(image_indices)
        return manager, response


if __name__ == "__main__":
    loader = MTGDeckLoader(r"G:\Documents\MixedProjects\LegacyGwentFromReceiptPrinter\server\decks\mtg")
    print(loader.get_deck_names())
    loader.load_deck(loader.get_deck_names()[0])
