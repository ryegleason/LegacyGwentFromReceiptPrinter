import json
import uuid

import web
import ThreadManager

ID_COOKIE_NAME = "uuid"

urls = ("/", "index",
        "/new", "new",
        "/play", "play",
        "/move", "move",
        "/tuck", "tuck",
        "/shuffle", "shuffle",
        "/draw", "draw",
        "/simple_action", "simple_action",
        "/sideboard", "sideboard",
        "/wish", "wish",
        "/shop_reload", "shop_reload",
        "/shop", "shop")
render = web.template.render('web/templates/')

user_deck_managers = {}


class index:
    def GET(self):
        has_active_game = False
        if web.cookies().get(ID_COOKIE_NAME) is not None:
            has_active_game = web.cookies().get(ID_COOKIE_NAME) in user_deck_managers
        else:
            web.setcookie(ID_COOKIE_NAME, str(uuid.uuid4()))
        return render.welcome(ThreadManager.deck_manager_loaders, has_active_game)


class new:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        deck = web.input().deck.split(" - ")
        user_deck_managers[user_id] = ThreadManager.deck_manager_loaders[deck[0]].load_deck(deck[1])
        raise web.seeother("/play")


class play:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        return render.play(user_deck_managers[user_id])


class move:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        source = web.input().source_zone
        destination = web.input().target_zone
        card_id = uuid.UUID(web.input().uuid)
        from_top = bool(web.input().get("from_top", False))
        num_down = int(web.input().get("num_down", 0))
        if not user_deck_managers[user_id].move(source, destination, card_id, from_top, num_down):
            raise web.BadRequest("Move failed, probably because that card isn't in the source zone.")
        raise web.seeother("/play")

    def GET(self):
        return self.POST()


class tuck:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        card_id = uuid.UUID(web.input().uuid)
        return render.tuck(user_deck_managers[user_id].card_for_uuid(card_id))


class shuffle:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        user_deck_managers[user_id].shuffle()
        raise web.seeother("/play")


class draw:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        draw_output = user_deck_managers[user_id].draw(web.input().draw_to)
        if draw_output:
            return json.dumps({"uuid": None if draw_output[0] is None else str(draw_output[0]),
                               "new_cards": [{"uuid": card.uuid, "image_url": card.card_data.get_card_image_uri(),
                                              "name": card.card_data.name, "zone": zone} for card, zone in
                                             draw_output[1]]})
        else:
            raise web.BadRequest("Draw failed, probably because the deck is empty.")


class simple_action:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        for action in user_deck_managers[user_id].simple_actions:
            if action.url == web.input().action:
                action.action()
                raise web.seeother("/play")
        raise web.BadRequest("Unknown simple action.")

    def POST(self):
        return self.GET()


class wish:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        return render.extra_zone("Sideboard", "sideboard", user_deck_managers[user_id].get_sideboard())


class sideboard:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        return render.sideboard(user_deck_managers[user_id], sorted)

    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        kwargs = {"to_deck[]": [], "to_sideboard[]": []}
        data = web.input(**kwargs)
        to_deck_uuids = list(uuid.UUID(uuid_str) for uuid_str in data.get("to_deck[]"))
        to_sideboard_uuids = list(uuid.UUID(uuid_str) for uuid_str in data.get("to_sideboard[]"))
        if user_deck_managers[user_id].sideboard_deck(to_deck_uuids, to_sideboard_uuids):
            raise web.seeother("/play")
        else:
            raise web.BadRequest(
                "Sideboarding failed, probably because you tried to move a card in the sideboard to the sideboard or a card in the deck to the deck.")


class shop_reload:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        user_deck_managers[user_id].refresh_shop(web.input().get("hold") == "true")
        raise web.seeother("/shop")


class shop:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        return render.shop(user_deck_managers[user_id])


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
