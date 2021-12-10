import datetime

import zmq

import os.path

import util
from daemons.CLIDaemon import CLIDaemon
from data import MTGCardData, ArtifactCardData, PokemonCardData
from data.ArtifactDeckLoader import ArtifactDeckLoader
from data.MTGDeckLoader import MTGDeckLoader
from daemons.PrinterDaemon import PrinterDaemon
from data.PokemonDeckLoader import PokemonDeckLoader
from proto.protobuf import reqrep_pb2


LOG = True
LOG_FILE_NAME = datetime.datetime.now().strftime("receipt_server_log_%Y_%m_%d_%H_%M_%f.txt")

context = zmq.Context()
server = context.socket(zmq.REP)
server.bind("tcp://*:27068")

printer_daemon = PrinterDaemon()
printer_daemon.setDaemon(True)
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

user_deck_managers = {}

decks_info_list = []

for game_name, loader in deck_manager_loaders.items():
    for deck_name in loader.get_deck_names():
        deck = reqrep_pb2.DecksInfo.DeckInfo()
        deck.name = deck_name
        deck.game = game_name
        decks_info_list.append(deck)

log_file = None
if LOG:
    log_file = open(LOG_FILE_NAME, 'w')

while True:
    request = server.recv()
    proto_request = reqrep_pb2.Req()
    proto_request.ParseFromString(request)

    if LOG:
        log_file.write(str(proto_request) + "\n")

    proto_response = reqrep_pb2.Rep()

    user_uuid = util.proto_UUID_to_UUID(proto_request.user_uuid)
    if proto_request.req_type == reqrep_pb2.Req.ReqType.DECKS_LIST:
        proto_response.success = True
        proto_response.decks_info.decks.extend(decks_info_list)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SELECT_DECK:
        deck_info = decks_info_list[proto_request.deck_index]
        user_deck_managers[user_uuid], proto_response = deck_manager_loaders[deck_info.game].load_deck(deck_info.name)
        cli_daemon.print_func = card_print_functions[deck_info.game]
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SHUFFLE:
        proto_response = user_deck_managers[user_uuid].shuffle()
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.DRAW:
        proto_response = user_deck_managers[user_uuid].draw(proto_request.draw_to)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.MOVE:
        proto_response = user_deck_managers[user_uuid].move(proto_request.move)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SPECIAL:
        proto_response = user_deck_managers[user_uuid].special(proto_request.special)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.RESUME:
        proto_response = user_deck_managers[user_uuid].get_full_state()
    else:
        proto_response.success = False

    if LOG:
        log_file.write(str(proto_response) + "\n")
        log_file.flush()

    server.send(proto_response.SerializeToString())
