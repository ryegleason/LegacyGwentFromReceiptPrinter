import uuid


class Card:

    def __init__(self, card_data):
        self.card_data = card_data
        self.uuid = uuid.uuid4()

    def print_self(self, printer):
        self.card_data.print_self(printer)

    def __lt__(self, other):
        return self.uuid < other.uuid


class DummyCard(Card):

    def __init__(self, set_uuid):
        self.uuid = set_uuid
