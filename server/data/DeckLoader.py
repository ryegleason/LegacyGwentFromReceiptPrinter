from typing import List

from data import DeckManager
from proto.protobuf import reqrep_pb2


class DeckLoader:

    def __init__(self, print_queue):
        self.print_queue = print_queue

    def get_deck_names(self) -> List[str]:
        pass

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        pass
