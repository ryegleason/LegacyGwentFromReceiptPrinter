import util
from proto.protobuf import reqrep_pb2
from proto.protobuf.reqrep_pb2 import Zone, Rep, Move, SpecialAction


def add_new_card_to_message(card, zone, response):
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

    def draw(self, draw_to: Zone) -> Rep:
        pass

    def move(self, move: Move) -> Rep:
        pass

    def special(self, special_action: SpecialAction):
        proto_response = reqrep_pb2.Rep()
        proto_response.success = False
        return proto_response

    def get_full_state(self) -> Rep:
        pass
