from typing import List

from data import DeckManager


class DeckLoader:

    def __init__(self, print_queue):
        self.print_queue = print_queue

    def get_deck_names(self) -> List[str]:
        pass

    def load_deck(self, name: str) -> DeckManager:
        pass
