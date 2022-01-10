import random

from data.DeckManager import add_new_card_to_message
from data.FiniteDeckManager import FiniteDeckManager
from proto.protobuf import reqrep_pb2
from proto.protobuf.reqrep_pb2 import SpecialAction, Zone

PRIZE_CARDS = 6


class PokemonDeckManager(FiniteDeckManager):

    def __init__(self, print_queue, decklist):
        super().__init__(print_queue, decklist, starting_hand_size=7)
        self.prize_cards = []

    def setup(self) -> reqrep_pb2.Rep:
        rep = super().setup()
        for i in range(PRIZE_CARDS):
            if len(self.deck) <= 0:
                rep.success = False
                return rep
            self.prize_cards.append(self.deck.pop())

        return self.get_full_state()

    def special(self, special_action: SpecialAction):
        rep = reqrep_pb2.Rep()
        rep.success = False
        if special_action == SpecialAction.DRAW_PRIZE_CARD:
            if len(self.prize_cards) == 0:
                return rep
            drawn_card = self.prize_cards.pop()
            self.hand.append(drawn_card)
            add_new_card_to_message(drawn_card, Zone.HAND, rep)
            rep.success = True
        return rep

    def get_full_state(self) -> reqrep_pb2.Rep:
        rep = super().get_full_state()
        rep.special_actions.extend([SpecialAction.DRAW_PRIZE_CARD])
        return rep
