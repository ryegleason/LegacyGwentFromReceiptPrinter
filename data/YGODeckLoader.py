from data.DeckLoaderGlob import DeckLoaderGlob
from data.YGODeckManager import YGODeckManager


class YGODeckLoader(DeckLoaderGlob):

    def load_deck(self, name: str) -> YGODeckManager:
        decklist = []
        sideboard = []
        is_sideboard = False

        with open(os.path.join(self.deck_dir, name + "." + self.suffix), "r") as f:
            for line in f:
                if line.strip() == "":
                    if is_sideboard:
                        break
                    else:
                        is_sideboard = True
                        continue

                copies = int(line.split(" ")[0])
                # Split and double sided card handling
                name = line[line.index(" "):].replace("/", " // ").strip()

                card_data = self.card_data_from_name(name)

                for i in range(copies):
                    new_card = Card(card_data)
                    if is_sideboard:
                        sideboard.append(new_card)
                    else:
                        decklist.append(new_card)

        manager = YGODeckManager(self.print_queue, decklist, sideboard)
        manager.setup()
        return manager
