import uuid

from data import CardData


class Card:

    def __init__(self, card_data: CardData):
        self.card_data = card_data
        self.uuid = uuid.uuid4()

    def queue_print(self, print_queue):
        self.card_data.queue_print(print_queue)

    def __lt__(self, other):
        return self.uuid < other.uuid


class DummyCard(Card):

    def __init__(self, set_uuid):
        self.uuid = set_uuid
