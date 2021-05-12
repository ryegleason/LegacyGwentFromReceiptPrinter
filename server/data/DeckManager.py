from escpos.escpos import Escpos

from proto.protobuf import reqrep_pb2
from proto.protobuf.reqrep_pb2 import Zone, Rep, Move, SpecialAction


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
