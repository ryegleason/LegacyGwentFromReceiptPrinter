import random
import uuid
from bisect import bisect_left
from typing import List, Tuple
from uuid import UUID

import util
from data import Card
from data.Card import DummyCard
from data.DeckManager import DeckManager, add_new_card_to_message
from proto.protobuf import reqrep_pb2
from proto.protobuf.reqrep_pb2 import Rep


class FiniteDeckManager(DeckManager):

    def __init__(self, print_queue, decklist: List[Card.Card], sideboard: List[Card.Card], starting_hand_size=7):
        super().__init__(print_queue)
        self.decklist = decklist
        self.sideboard_list = sideboard
        self.starting_hand_size = starting_hand_size
        self.decklist.sort()
        self.sideboard_list.sort()
        self.deck: List[Card] = []
        self.hand: List[Card] = []
        self.played: List[Card] = []
        self.sideboard: List[Card] = []
        self.special_actions["mulligan"] = True
        if len(self.sideboard_list) > 0:
            self.special_actions["sideboard"] = True
            self.special_actions["wish"] = True

    def setup(self) -> bool:
        self.deck = random.sample(self.decklist, len(self.decklist))
        self.sideboard = sorted(self.sideboard_list, key=lambda c: c.card_data.name)
        self.hand = []
        self.played = []

        success = True
        for i in range(self.starting_hand_size):
            success = success and self.draw("hand") is not False

        return success

    def shuffle(self) -> reqrep_pb2.Rep:
        random.shuffle(self.deck)
        response = reqrep_pb2.Rep()
        response.success = True
        return response

    def draw(self, draw_to: str) -> bool | Tuple[uuid.UUID, List[Tuple[Card.Card, str]]]:
        if draw_to == "deck" or len(self.deck) < 1:
            return False

        to_draw = self.deck.pop()
        if draw_to == "hand":
            self.hand.append(to_draw)
        elif draw_to == "played":
            self.played.append(to_draw)
            to_draw.queue_print(self.print_queue)
        else:
            return False

        return to_draw.uuid, []

    def move(self, source_zone: str, target_zone: str, card_uuid: uuid.UUID, from_top: bool = False, num_down: int = 0) -> bool:
        try:
            card = self.card_for_uuid(card_uuid)
            if source_zone == "hand":
                self.hand.remove(card)
            elif source_zone == "played":
                self.played.remove(card)
            elif source_zone == "sideboard":
                self.sideboard.remove(card)
            else:
                self.deck.remove(card)
        except ValueError:
            return False

        return self.move_card(card, target_zone, from_top, num_down)

    def get_deck(self) -> List[Card.Card]:
        # Sort alphabetically, for convenience and to avoid exposing deck order
        return sorted(self.deck, key=lambda c: c.card_data.name)

    def get_hand(self) -> List[Card.Card]:
        return self.hand

    def get_played(self) -> List[Card.Card]:
        return self.played

    def get_sideboard(self) -> List[Card.Card]:
        return self.sideboard

    def put_in_deck(self, card: Card, from_top: bool, n_cards_down: int = 0):
        if from_top and n_cards_down == 0:
            self.deck.append(card)
        else:
            insert_index = -n_cards_down if from_top else n_cards_down
            # Bound properly
            insert_index = max(-len(self.deck), insert_index)
            insert_index = min(insert_index, len(self.deck))
            self.deck.insert(insert_index, card)

    def card_for_uuid(self, uuid: UUID) -> Card:
        i = bisect_left(self.decklist, DummyCard(uuid))
        if i != len(self.decklist) and self.decklist[i].uuid == uuid:
            return self.decklist[i]
        i = bisect_left(self.sideboard_list, DummyCard(uuid))
        if i != len(self.sideboard_list) and self.sideboard_list[i].uuid == uuid:
            return self.sideboard_list[i]
        raise ValueError

    def move_card(self, card: Card, target_zone: str, from_top: bool = False, num_down: int = 0) -> bool:
        if target_zone == "hand":
            self.hand.append(card)
        elif target_zone == "played":
            self.played.append(card)
            card.queue_print(self.print_queue)
        elif target_zone == "deck":
            self.put_in_deck(card, from_top, num_down)
        else:
            return False
        return True

    def mulligan(self) -> bool:
        if len(self.hand) != self.starting_hand_size or len(self.played) != 0:
            return False
        return self.setup()