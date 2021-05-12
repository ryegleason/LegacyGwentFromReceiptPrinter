import os
from typing import List

from data.ArtifactCardData import ArtifactCardData
from data.ArtifactDeckDecoder import MyArtifactDeckDecoder
from data.ArtifactDeckManager import ArtifactDeckManager
from data.Card import Card
from data.CardData import CardData
from data.DeckLoader import DeckLoader
from data.DeckManager import DeckManager
from proto.protobuf import reqrep_pb2


class ArtifactDeckLoader(DeckLoader):

    def __init__(self, print_queue, deck_codes_file):
        super().__init__(print_queue)
        decoder = MyArtifactDeckDecoder()
        self.decks = {}
        if os.path.isfile(deck_codes_file):
            with open(deck_codes_file, "r") as f:
                for line in f:
                    if line.strip() != "":
                        deck = decoder.ParseDeck(line.strip())
                        self.decks[deck["name"]] = deck

    def get_deck_names(self) -> List[str]:
        return list(self.decks.keys())

    def load_deck(self, name: str) -> (DeckManager, reqrep_pb2.Rep):
        deck = self.decks[name]
        heroes = deck["heroes"]
        other = deck["cards"]

        hero_card_data: List[CardData] = [None] * 2
        main_deck_cards = []
        item_deck_cards = []

        for card in other:
            new_card = ArtifactCardData(card[0])
            if new_card.is_item():
                item_deck_cards.append((new_card, card[1]))
            else:
                main_deck_cards.append((new_card, card[1]))

        for hero in heroes:
            hero_card = ArtifactCardData(hero[0])
            if hero[1] == 1:
                hero_card_data.insert(0, hero_card)
            else:
                # 3 -> -1, 2 -> -2
                hero_card_data[(-4 + hero[1])] = hero_card

            for include in hero_card.includes:
                main_deck_cards.append((ArtifactCardData(include[0]), include[1]))

        deck_cards = []
        item_cards = []

        for (card_data, copies) in main_deck_cards:
            for i in range(copies):
                deck_cards.append(Card(card_data))

        for (card_data, copies) in item_deck_cards:
            for i in range(copies):
                item_cards.append(Card(card_data))

        manager = ArtifactDeckManager(self.print_queue, deck_cards, hero_card_data, item_cards)
        response = manager.setup()
        return manager, response

