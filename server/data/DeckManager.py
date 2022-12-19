import uuid
from typing import List

import util
from data import Card
from proto.protobuf import reqrep_pb2
from proto.protobuf.reqrep_pb2 import Zone, Rep, Move, SpecialAction


def add_new_card_to_message(card: Card.Card, zone: Zone, response: Rep):
    move = response.moves.add()
    proto_card = response.new_cards.add()
    util.UUID_to_proto_UUID(card.uuid, move.card_uuid)
    util.UUID_to_proto_UUID(card.uuid, proto_card.card_uuid)
    move.source_zone = reqrep_pb2.Zone.NONE
    move.target_zone = zone
    proto_card.image_uri = card.card_data.get_card_image_uri()


class DeckManager:

    def __init__(self, print_queue):
        self.print_queue = print_queue

    def shuffle(self) -> Rep:
        pass

    def draw(self, draw_to: str) -> Rep:
        pass

    def move(self, source_zone: str, target_zone: str, card_uuid: uuid.UUID, from_top: bool, num_down: int) -> bool:
        pass

    def special(self, special_action: SpecialAction):
        proto_response = reqrep_pb2.Rep()
        proto_response.success = False
        return proto_response

    def get_deck(self) -> List[Card.Card]:
        """
        Get the deck *for display purposes.* This means the deck should probably be g.g. sorted alphabetically before
        being returned, so deck order isn't exposed.
        :return: The deck, in an order suitable for displaying to players.
        """
        pass

    def get_hand(self) -> List[Card.Card]:
        pass

    def get_played(self) -> List[Card.Card]:
        pass

    def get_full_state(self) -> Rep:
        response = reqrep_pb2.Rep()

        for card in self.get_deck():
            add_new_card_to_message(card, reqrep_pb2.Zone.DECK, response)
        for card in self.get_hand():
            add_new_card_to_message(card, reqrep_pb2.Zone.HAND, response)
        for card in self.get_played():
            add_new_card_to_message(card, reqrep_pb2.Zone.PLAYED, response)

        response.success = True
        return response
