import random
from bisect import bisect_left
from typing import List
from uuid import UUID

import util
from data import Card
from data.Card import DummyCard
from data.DeckManager import DeckManager
from proto.protobuf import reqrep_pb2


class FiniteDeckManager(DeckManager):

    def __init__(self, print_queue, decklist, starting_hand_size=7):
        super().__init__(print_queue)
        self.decklist = decklist
        self.starting_hand_size = starting_hand_size
        self.decklist.sort()
        self.deck: List[Card] = []
        self.hand: List[Card] = []
        self.played: List[Card] = []

    def setup(self) -> reqrep_pb2.Rep:
        self.deck = random.sample(self.decklist, len(self.decklist))
        self.hand = []
        self.played = []

        response = reqrep_pb2.Rep()
        response.success = True
        for i in range(self.starting_hand_size):
            response.success = response.success and self.draw(reqrep_pb2.Zone.HAND).success

        # Sort alphabetically, for convenience and to avoid exposing deck order
        for card in sorted(self.deck, key=lambda c: c.card_data.name):
            move = response.moves.add()
            util.UUID_to_proto_UUID(card.uuid, move.card_uuid)
            move.source_zone = reqrep_pb2.Zone.NONE
            move.target_zone = reqrep_pb2.Zone.DECK
        for card in self.hand:
            move = response.moves.add()
            util.UUID_to_proto_UUID(card.uuid, move.card_uuid)
            move.source_zone = reqrep_pb2.Zone.NONE
            move.target_zone = reqrep_pb2.Zone.HAND

        return response

    def shuffle(self) -> reqrep_pb2.Rep:
        random.shuffle(self.deck)
        response = reqrep_pb2.Rep()
        response.success = True
        return response

    def draw(self, draw_to: reqrep_pb2.Zone) -> reqrep_pb2.Rep:
        response = reqrep_pb2.Rep()
        if draw_to == reqrep_pb2.Zone.DECK or len(self.deck) < 1:
            response.success = False
            return response

        to_draw = self.deck.pop()
        if draw_to == reqrep_pb2.Zone.HAND:
            self.hand.append(to_draw)
        elif draw_to == reqrep_pb2.Zone.PLAYED:
            self.played.append(to_draw)
            to_draw.queue_print(self.print_queue)
        else:
            response.success = False
            return response

        move = response.moves.add()
        util.UUID_to_proto_UUID(to_draw.uuid, move.card_uuid)
        move.source_zone = reqrep_pb2.Zone.DECK
        move.target_zone = draw_to
        response.success = True
        return response

    def move(self, move: reqrep_pb2.Move) -> reqrep_pb2.Rep:
        response = reqrep_pb2.Rep()

        try:
            card = self.card_for_uuid(util.proto_UUID_to_UUID(move.card_uuid))
            if move.source_zone == reqrep_pb2.Zone.HAND:
                self.hand.remove(card)
            elif move.source_zone == reqrep_pb2.Zone.PLAYED:
                self.played.remove(card)
            else:
                self.deck.remove(card)
        except ValueError:
            response.success = False
            return response

        if not self.move_card(card, move):
            response.success = False
            return response

        response.success = True
        response.moves.append(move)
        return response

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
        raise ValueError

    def move_card(self, card: Card, move: reqrep_pb2.Move) -> bool:
        if move.target_zone == reqrep_pb2.Zone.HAND:
            self.hand.append(card)
        elif move.target_zone == reqrep_pb2.Zone.PLAYED:
            self.played.append(card)
            card.queue_print(self.print_queue)
        elif move.target_zone == reqrep_pb2.Zone.DECK:
            self.put_in_deck(card, move.from_top, move.num_down)
        else:
            return False
        return True
