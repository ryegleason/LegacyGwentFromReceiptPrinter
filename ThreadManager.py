import datetime
import os.path

from daemons.CLIDaemon import CLIDaemon
from daemons.PrinterDaemon import PrinterDaemon
from data import MTGCardData, ArtifactCardData, PokemonCardData
from data.ArtifactDeckLoader import ArtifactDeckLoader
from data.MTGDeckLoader import MTGDeckLoader
from data.PokemonDeckLoader import PokemonDeckLoader

LOG = True
LOG_FILE_NAME = datetime.datetime.now().strftime("receipt_server_log_%Y_%m_%d_%H_%M_%f.txt")

printer_daemon = PrinterDaemon()
printer_daemon.daemon = True
printer_daemon.start()
print_queue = printer_daemon.print_queue

deck_manager_loaders = {"mtg": MTGDeckLoader(print_queue, os.path.abspath(os.path.join("decks", "mtg"))),
                        "artifact": ArtifactDeckLoader(print_queue, os.path.abspath(os.path.join("decks", "artifact_decks.txt"))),
                        "pokemon": PokemonDeckLoader(print_queue, os.path.abspath(os.path.join("decks", "pokemon")))}

card_print_functions = {"mtg": MTGCardData.print_card_from_name, "artifact": ArtifactCardData.print_card_from_name,
                        "pokemon": PokemonCardData.print_card_from_name}

cli_daemon = CLIDaemon(print_queue)
cli_daemon.start()
cli_daemon.print_func = card_print_functions["mtg"]
