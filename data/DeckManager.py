import uuid
from collections import namedtuple
from typing import List, Tuple, Dict

from data import Card

SimpleAction = namedtuple("SimpleAction", ["description", "url", "redirect", "action"])

class DeckManager:

    def __init__(self, print_queue):
        self.print_queue = print_queue
        self.simple_actions: List = []
        self.complex_actions: Dict[str, str] = {} # map of complex action button texts to URLs

    def shuffle(self):
        pass

    def draw(self, draw_to: str) -> bool | Tuple[uuid.UUID, List[Tuple[Card.Card, str]]]:
        """
        Draw a card from the deck to the specified zone.
        :param draw_to: The zone to draw to. Must be one of "deck", "hand", or "played".
        :return: False if the draw fails. Otherwise, the uuid of the card drawn (may be None) and a list of tuple pairs
        of (card, zone) representing any new cards created and what zone they were created in.
        """
        pass

    def move(self, source_zone: str, target_zone: str, card_uuid: uuid.UUID, from_top: bool, num_down: int) -> bool:
        pass

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
