import random
from bisect import bisect_left
from typing import List
from uuid import UUID

from escpos.escpos import Escpos

from data import Card


class Player:

    def __init__(self, decklist: List[Card], printer: Escpos):
        self.decklist = decklist
        self.decklist.sort()
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

    def play_from_hand(self, card_id: UUID):
        card = self.card_for_uuid(card_id)
        self.hand.remove(card)
        self.played.append(card)
        self.played[-1].print_self(self.printer)

    def play_from_deck(self, card_id: UUID):
        card = self.card_for_uuid(card_id)
        self.deck.remove(card)
        self.played.append(card)
        self.played[-1].print_self(self.printer)

    def play_from_deck_blind(self, top_card: bool) -> bool:
        if len(self.deck) == 0:
            return False
        remove_index = -1 if top_card else 0
        self.played.append(self.deck.pop(remove_index))
        self.played[-1].print_self(self.printer)
        return True

    def return_to_hand(self, card_id: UUID):
        card = self.card_for_uuid(card_id)
        self.played.remove(card)
        self.hand.append(card)

    def return_to_deck_from_play(self, card_id: UUID, from_top: bool, n_cards_down: int = 0):
        card = self.card_for_uuid(card_id)
        self.played.remove(card)
        if from_top and n_cards_down == 0:
            self.deck.append(card)
        else:
            insert_index = -n_cards_down if from_top else n_cards_down
            self.deck.insert(insert_index, card)

    def return_to_deck_from_hand(self, card_id: UUID, from_top: bool, n_cards_down: int = 0):
        card = self.card_for_uuid(card_id)
        self.hand.remove(card)
        if from_top and n_cards_down == 0:
            self.deck.append(card)
        else:
            insert_index = -n_cards_down if from_top else n_cards_down
            self.deck.insert(insert_index, card)

    def tutor(self, card_id: UUID):
        card = self.card_for_uuid(card_id)
        self.deck.remove(card)
        self.hand.append(card)
        self.shuffle()

    def card_for_uuid(self, uuid: UUID) -> Card:
        i = bisect_left(self.decklist, uuid)
        if i != len(self.decklist) and self.decklist[i].uuid == uuid:
            return self.decklist[i]
        raise ValueError
