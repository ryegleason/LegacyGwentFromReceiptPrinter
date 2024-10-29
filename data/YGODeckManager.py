from typing import List

from data import Card
from data.FiniteDeckManager import FiniteDeckManager


class YGODeckManager(FiniteDeckManager):

    def __init__(self, print_queue, decklist: List[Card.Card], extra_deck_list: List[Card.Card], sideboard: List[Card.Card]):
        super().__init__(print_queue, decklist, sideboard, starting_hand_size=5)
        self.extra_deck_list = extra_deck_list
        self.extra_deck = []
        self.complex_actions["Extra Deck"] = "extra_deck"

    def setup(self) -> bool:
        if not super().setup():
            return False

        self.extra_deck = sorted(self.extra_deck_list, key=lambda c: c.card_data.name)

        return True