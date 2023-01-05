import json
from typing import List
from urllib.parse import quote

from data import MTGCardData
from data.Card import Card
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from data.InfiniteDeckManager import InfiniteDeckManager


class RandomMTGDeckLoader(DeckLoader):

    def get_deck_names(self) -> List[str]:
        return ["f:vintage"]

    def load_deck(self, name: str) -> DeckManager:
        def get_card_function() -> Card:
            # exclude nonsnow basics
            query = "https://api.scryfall.com/cards/random/?q=" + quote("(-t:basic or t:snow) " + name)
            response = json.loads(MTGCardData.request_from_scryfall(query).content)
            return Card(MTGCardData.MTGCardData(response))
        deck_manager = InfiniteDeckManager(self.print_queue, get_card_function)
        deck_manager.setup()
        return deck_manager
