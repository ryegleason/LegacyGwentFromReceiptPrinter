from typing import Dict
from uuid import UUID

import zmq
from escpos.printer import Dummy, Usb

import util
from data import DeckManager
from data.ArtifactDeckLoader import ArtifactDeckLoader
from data.MTGDeckLoader import MTGDeckLoader
from printer.PrinterDaemon import PrinterDaemon
from proto.protobuf import reqrep_pb2
import os.path


context = zmq.Context()
server = context.socket(zmq.REP)
server.bind("tcp://*:27068")

printer_daemon = PrinterDaemon()
printer_daemon.setDaemon(True)
printer_daemon.start()
print_queue = printer_daemon.print_queue

deck_manager_loaders = {"mtg": MTGDeckLoader(print_queue, os.path.abspath(os.path.join("decks", "mtg"))),
                        "artifact": ArtifactDeckLoader(print_queue, os.path.abspath(os.path.join("decks", "artifact_decks.txt")))}
user_deck_managers = {}

decks_info_list = []

for game_name, loader in deck_manager_loaders.items():
    for deck_name in loader.get_deck_names():
        deck = reqrep_pb2.DecksInfo.DeckInfo()
        deck.name = deck_name
        deck.game = game_name
        decks_info_list.append(deck)

while True:
    request = server.recv()
    proto_request = reqrep_pb2.Req()
    proto_request.ParseFromString(request)

    proto_response = reqrep_pb2.Rep()

    user_uuid = util.proto_UUID_to_UUID(proto_request.user_uuid)
    if proto_request.req_type == reqrep_pb2.Req.ReqType.DECKS_LIST:
        proto_response.success = True
        proto_response.decks_info.decks.extend(decks_info_list)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SELECT_DECK:
        deck_info = decks_info_list[proto_request.deck_index]
        user_deck_managers[user_uuid], proto_response = deck_manager_loaders[deck_info.game].load_deck(deck_info.name)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SHUFFLE:
        proto_response = user_deck_managers[user_uuid].shuffle()
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.DRAW:
        proto_response = user_deck_managers[user_uuid].draw(proto_request.draw_to)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.MOVE:
        proto_response = user_deck_managers[user_uuid].move(proto_request.move)
    elif proto_request.req_type == reqrep_pb2.Req.ReqType.SPECIAL:
        proto_response = user_deck_managers[user_uuid].special(proto_request.special)
    else:
        proto_response.success = False

    # print("Response sent: \n" + str(proto_response))

    # print("Response success: " + str(proto_response.success))
    server.send(proto_response.SerializeToString())
