import io
import os
from pathlib import Path
from typing import List

import util
from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from data.MTGCardData import MTGCardData
from data.MTGDeckManager import MTGDeckManager
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
        proto_cards = reqrep_pb2.Cards()
        image_index = 0

        with open(os.path.join(self.deck_dir, name + ".txt"), "r") as f:
            for line in f:
                if line.strip() == "":
                    break
                copies = int(line.split(" ")[0])
                # Split and double sided card handling
                name = line[line.index(" "):].replace("/", " // ")

                card_data = MTGCardData(name)

                # Convert image to bytes
                img_byte_arr = io.BytesIO()
                card_data.get_card_image().save(img_byte_arr, format='PNG')
                proto_cards.images.append(img_byte_arr.getvalue())

                for i in range(copies):
                    new_card = Card(card_data)
                    cards.append(new_card)
                    proto_cards.card_uuids.append(util.UUID_to_proto_UUID(new_card.uuid))
                    proto_cards.image_indices.append(image_index)

                image_index += 1

        manager = MTGDeckManager(cards)
        response = manager.setup()
        response.new_cards = proto_cards
        return manager, response

