from uuid import UUID

from escpos.escpos import Escpos

from proto.protobuf.reqrep_pb2 import Zone, Rep, Move


class DeckManager:

    def __init__(self):
        self.printer = None

    def shuffle(self) -> Rep:
        pass

    def draw(self, draw_from: Zone) -> Rep:
        pass

    def move(self, move: Move) -> Rep:
        pass

    def set_printer(self, printer: Escpos):
        self.printer = printer
