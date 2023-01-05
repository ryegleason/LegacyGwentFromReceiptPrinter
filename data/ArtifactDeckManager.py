import random
import uuid
from uuid import UUID

from escpos.printer import Dummy

from data.ArtifactCardData import ArtifactCardData, id_to_card_dict
from data.Card import Card
from data.DeckManager import SimpleAction
from data.FiniteDeckManager import FiniteDeckManager

CREEP_CARD = ArtifactCardData(1006)
CONSUMABLE_SHOP_CARDS = [ArtifactCardData(3003), ArtifactCardData(3004), ArtifactCardData(3005), ArtifactCardData(3006)]
SECRET_SHOP_CARDS = []
for card_id, card_data in id_to_card_dict.items():
    if card_data["card_type"] == "Item" and not (3003 <= card_id <= 3006):
        SECRET_SHOP_CARDS.append(ArtifactCardData(card_id))

dummy_printer = Dummy()
dummy_printer.set(align="center")
dummy_printer.text("\n" * 5)
dummy_printer.text("<-------\nL")
dummy_printer.text("\n" * 4)
left_arrow_raw = dummy_printer.output

dummy_printer = Dummy()
dummy_printer.set(align="center")
dummy_printer.text("\n" * 5)
dummy_printer.text("------->\nR")
dummy_printer.text("\n" * 4)
right_arrow_raw = dummy_printer.output

dummy_printer = Dummy()
dummy_printer.set(align="center")
dummy_printer.text("\n" * 4)
dummy_printer.text("|\n|\nV")
dummy_printer.text("\n" * 4)
forward_arrow_raw = dummy_printer.output


class ArtifactDeckManager(FiniteDeckManager):

    def __init__(self, print_queue, main_deck, heroes, item_deck):
        super().__init__(print_queue, main_deck, [], starting_hand_size=5)

        self.simple_actions.append(SimpleAction("Print Creep", "creep", False, self.print_creep))
        self.simple_actions.append(SimpleAction("Random Arrow", "random_arrow", False, self.print_random_arrow))
        self.simple_actions.append(SimpleAction("Left Arrow", "left_arrow", False, self.print_left_arrow))
        self.simple_actions.append(SimpleAction("Right Arrow", "right_arrow", False, self.print_right_arrow))
        self.simple_actions.append(SimpleAction("Forward Arrow", "forward_arrow", False, self.print_forward_arrow))

        self.complex_actions["Shop (Hold)"] = "shop_reload?hold=true"
        self.complex_actions["Shop (No Hold)"] = "shop_reload?hold=false"

        self.heroes = heroes
        self.starting_item_deck = item_deck
        self.item_deck = []
        self.secret_shop_item = None
        # Order is always secret shop, item deck, consumable
        self.shop_cards = [None, None, None]
        self.item_card_uuids_map = {}
        for card in item_deck:
            self.item_card_uuids_map[card.uuid.int] = card

    def setup(self) -> bool:
        if not super().setup():
            return False

        self.item_deck = random.sample(self.starting_item_deck, len(self.starting_item_deck))
        self.secret_shop_item = random.choice(SECRET_SHOP_CARDS)

        # Randomize print order for first 3
        for starting_hero in random.sample(self.heroes[:3], 3):
            starting_hero.queue_print(self.print_queue)
        for hero in self.heroes[3:]:
            hero.queue_print(self.print_queue)

        return True

    def move(self, source_zone: str, target_zone: str, card_uuid: uuid.UUID, from_top: bool = False, num_down: int = 0) -> bool:
        if source_zone != "special":
            return super().move(source_zone, target_zone, card_uuid, from_top, num_down)

        try:
            card_idx = [idx for idx, value in enumerate(self.shop_cards) if value is not None and value.uuid == card_uuid][0]
        except IndexError:
            return False

        card = self.shop_cards[card_idx]
        if not self.move_card(card, target_zone, from_top, num_down):
            return False

        # Item deck, so we replace it
        if card_idx == 1:
            self.item_deck.pop()
            if len(self.item_deck) > 0:
                new_card = self.item_deck[-1]
                self.shop_cards[1] = new_card
            else:
                self.shop_cards[1] = None
        else:
            self.shop_cards[card_idx] = None

        # Remove secret shop item if it was bought, so it can't be held
        if card_idx == 0:
            self.secret_shop_item = None

        return True

    def print_creep(self):
        CREEP_CARD.queue_print(self.print_queue)

    def print_random_arrow(self):
        self.print_queue.put(random.choice([left_arrow_raw, right_arrow_raw, forward_arrow_raw]))

    def print_left_arrow(self):
        self.print_queue.put(left_arrow_raw)

    def print_right_arrow(self):
        self.print_queue.put(right_arrow_raw)

    def print_forward_arrow(self):
        self.print_queue.put(forward_arrow_raw)

    def refresh_shop(self, hold: bool):
        if not hold or self.secret_shop_item is None:
            self.secret_shop_item = random.choice(SECRET_SHOP_CARDS)
        random.shuffle(self.item_deck)
        secret_shop_card = Card(self.secret_shop_item)
        consumable_card = Card(random.choice(CONSUMABLE_SHOP_CARDS))

        self.item_card_uuids_map[secret_shop_card.uuid.int] = secret_shop_card
        self.item_card_uuids_map[consumable_card.uuid.int] = consumable_card

        if len(self.item_deck) > 0:
            item_deck_card = self.item_deck[-1]
            self.shop_cards = [secret_shop_card, item_deck_card, consumable_card]
        else:
            self.shop_cards = [secret_shop_card, None, consumable_card]

    def card_for_uuid(self, uuid: UUID) -> Card:
        try:
            return self.item_card_uuids_map[uuid.int]
        except KeyError:
            return super().card_for_uuid(uuid)
