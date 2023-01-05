from data.FiniteDeckManager import FiniteDeckManager
from data.DeckManager import SimpleAction

PRIZE_CARDS = 6


class PokemonDeckManager(FiniteDeckManager):

    def __init__(self, print_queue, decklist):
        super().__init__(print_queue, decklist, [], starting_hand_size=7)
        self.prize_cards = []
        self.simple_actions.append(SimpleAction("Draw Prize Card", "prize", True, self.draw_prize_card))

    def setup(self) -> bool:
        if not super().setup():
            return False

        for i in range(PRIZE_CARDS):
            if len(self.deck) <= 0:
                return False
            self.prize_cards.append(self.deck.pop())

        return True

    def draw_prize_card(self) -> bool:
        if len(self.prize_cards) == 0:
            return False
        drawn_card = self.prize_cards.pop()
        self.hand.append(drawn_card)
        return True
