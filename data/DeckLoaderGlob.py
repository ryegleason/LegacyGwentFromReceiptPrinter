import os
from pathlib import Path
from typing import List

from data.DeckLoader import DeckLoader


class DeckLoaderGlob(DeckLoader):

    def __init__(self, print_queue, deck_dir, suffix="txt"):
        super().__init__(print_queue)
        self.deck_dir = deck_dir
        self.deck_names = []
        self.suffix = suffix
        if os.path.isdir(deck_dir):
            for deck_filename in Path(deck_dir).rglob("*." + suffix):
                self.deck_names.append(deck_filename.with_suffix('').name)

    def get_deck_names(self) -> List[str]:
        return self.deck_names
