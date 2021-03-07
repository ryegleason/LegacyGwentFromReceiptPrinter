import random
from typing import List

from escpos.escpos import Escpos

import Card


class Player:

    def __init__(self, decklist: List[Card], printer: Escpos):
        self.decklist = decklist
        self.printer = printer
        self.deck = []
        self.hand = []
        self.played = []
        self.reset()

    def reset(self):
        self.deck = random.sample(self.decklist, len(self.decklist))
        self.hand = []
        self.played = []

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self, n_cards=1) -> bool:
        if len(self.deck) < n_cards:
            return False
        for i in range(n_cards):
            self.hand.append(self.deck.pop())
        return True

    def play_from_hand(self, hand_index: int):
        self.played.append(self.hand.pop(hand_index))
        self.played[-1].print_self(self.printer)

    def play_from_deck(self, deck_index: int):
        self.played.append(self.deck.pop(deck_index))
        self.played[-1].print_self(self.printer)

    def play_from_deck_blind(self, top_card: bool) -> bool:
        if len(self.deck) == 0:
            return False
        remove_index = -1 if top_card else 0
        self.played.append(self.deck.pop(remove_index))
        self.played[-1].print_self(self.printer)
        return True

    def return_to_hand(self, played_index: int):
        self.hand.append(self.played.pop(played_index))

    def return_to_deck_from_play(self, played_index: int, from_top: bool, n_cards_down: int = 0):
        if from_top and n_cards_down == 0:
            self.deck.append(self.played.pop(played_index))
        else:
            insert_index = -n_cards_down if from_top else n_cards_down
            self.deck.insert(insert_index, self.played.pop(played_index))

    def return_to_deck_from_hand(self, hand_index: int, from_top: bool, n_cards_down: int = 0):
        if from_top and n_cards_down == 0:
            self.deck.append(self.hand.pop(hand_index))
        else:
            insert_index = -n_cards_down if from_top else n_cards_down
            self.deck.insert(insert_index, self.hand.pop(hand_index))

    def tutor(self, deck_index: int):
        self.hand.append(self.deck.pop(deck_index))
        self.shuffle()
