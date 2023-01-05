from uuid import UUID
from typing import Tuple, List, Callable

from data.Card import Card
from data.DeckManager import DeckManager


class InfiniteDeckManager(DeckManager):

    def __init__(self, print_queue, get_card: Callable[[], Card], starting_hand_size=7):
        super().__init__(print_queue)
        self.deck = []
        self.hand = []
        self.played = []
        self.get_card = get_card
        self.starting_hand_size = starting_hand_size

    def setup(self) -> bool:
        success = True
        for i in range(self.starting_hand_size):
            success = success and self.draw("hand")
        return success

    def shuffle(self):
        self.deck = []

    def draw(self, draw_to: str) -> bool | Tuple[UUID, List[Tuple[Card, str]]]:
        if len(self.deck) > 0:
            drawn_card = self.deck.pop()
            to_ret = (drawn_card.uuid, [])
        else:
            drawn_card = self.get_card()
            to_ret = (None, [(drawn_card, draw_to)])

        if draw_to == "hand":
            self.hand.append(drawn_card)
        elif draw_to == "played":
            self.played.append(drawn_card)
            drawn_card.queue_print(self.print_queue)
        else:
            return False

        return to_ret

    def move(self, source_zone: str, target_zone: str, card_uuid: UUID, from_top: bool = False, num_down: int = 0) -> bool:
        try:
            card = self.card_for_uuid(card_uuid)
            if source_zone == "hand":
                self.hand.remove(card)
            elif source_zone == "played":
                self.played.remove(card)
            else:
                self.deck.remove(card)

            if target_zone == "hand":
                self.hand.append(card)
            elif target_zone == "played":
                self.played.append(card)
                card.queue_print(self.print_queue)
            elif target_zone == "deck" and from_top:
                while len(self.deck) < num_down:
                    self.deck.insert(0, self.get_card())
                self.deck.insert(len(self.deck) - num_down, card)
            return True
        except ValueError:
            return False

    def get_deck(self) -> List[Card]:
        return self.deck

    def get_hand(self) -> List[Card]:
        return self.hand

    def get_played(self) -> List[Card]:
        return self.played

    def card_for_uuid(self, uuid: UUID) -> Card:
        for card in self.deck + self.hand + self.played:
            if card.uuid == uuid:
                return card
        raise ValueError
