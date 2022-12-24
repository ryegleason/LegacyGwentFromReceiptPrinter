import os
from pathlib import Path
from typing import List

from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckLoaderGlob import DeckLoaderGlob
from data.DeckManager import DeckManager
from data.FiniteDeckManager import FiniteDeckManager
from data.MTGCardData import MTGCardData
from proto.protobuf import reqrep_pb2


class MTGDeckLoader(DeckLoaderGlob):

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        maindeck = []
        sideboard = []
        is_sideboard = False

        with open(os.path.join(self.deck_dir, name + "." + self.suffix), "r") as f:
            for line in f:
                if line.strip() == "":
                    if is_sideboard:
                        break
                    else:
                        is_sideboard = True
                        continue

                copies = int(line.split(" ")[0])
                # Split and double sided card handling
                name = line[line.index(" "):].replace("/", " // ").strip()

                card_data = MTGCardData(name)

                for i in range(copies):
                    new_card = Card(card_data)
                    if is_sideboard:
                        sideboard.append(new_card)
                    else:
                        maindeck.append(new_card)

        manager = FiniteDeckManager(self.print_queue, maindeck, sideboard, starting_hand_size=7)
        response = manager.setup()
        return manager, response


if __name__ == "__main__":
    loader = MTGDeckLoader(r"G:\Documents\MixedProjects\LegacyGwentFromReceiptPrinter\server\decks\mtg")
    print(loader.get_deck_names())
    loader.load_deck(loader.get_deck_names()[0])
