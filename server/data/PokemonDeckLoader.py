import os

from data.Card import Card
from data.DeckLoaderGlob import DeckLoaderGlob
from data.DeckManager import DeckManager
from data.FiniteDeckManager import FiniteDeckManager
from data.PokemonCardData import PokemonCardData, BASIC_ENERGY
from data.PokemonDeckManager import PokemonDeckManager
from proto.protobuf import reqrep_pb2


class PokemonDeckLoader(DeckLoaderGlob):

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        cards = []

        with open(os.path.join(self.deck_dir, name + "." + self.suffix), "r") as f:
            for line in f:
                line = line.strip()
                if line == "" or line[0] == "#":
                    break
                split_line = line.split(" ")
                copies = int(split_line[0])

                if " ".join(split_line[1:3]) in BASIC_ENERGY:
                    card_data = BASIC_ENERGY[" ".join(split_line[1:3])]
                else:
                    set_code = split_line[-2]
                    card_number = split_line[-1]
                    card_data = PokemonCardData(set_code, card_number)

                for i in range(copies):
                    new_card = Card(card_data)
                    cards.append(new_card)

        manager = PokemonDeckManager(self.print_queue, cards)
        response = manager.setup()
        return manager, response


if __name__ == "__main__":
    loader = PokemonDeckLoader(r"G:\Documents\MixedProjects\LegacyGwentFromReceiptPrinter\server\decks\pokemon")
    print(loader.get_deck_names())
    loader.load_deck(loader.get_deck_names()[0])
