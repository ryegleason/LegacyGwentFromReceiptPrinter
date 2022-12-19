import uuid

import web
import main

ID_COOKIE_NAME = "uuid"

urls = ("/", "index",
        "/new", "new",
        "/play", "play",
        "/move", "move",
        "/tuck", "tuck",)
render = web.template.render('web/templates/')

class index:
    def GET(self):
        has_active_game = False
        if web.cookies().get(ID_COOKIE_NAME) is not None:
            has_active_game = web.cookies().get(ID_COOKIE_NAME) in main.user_deck_managers
        else:
            web.setcookie(ID_COOKIE_NAME, str(uuid.uuid4()))
        return render.welcome(main.deck_manager_loaders, has_active_game)

class new:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        deck = web.input().deck.split(" - ")
        main.user_deck_managers[user_id], _ = main.deck_manager_loaders[deck[0]].load_deck(deck[1])
        raise web.seeother("/play")

class play:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        return render.play(main.user_deck_managers[user_id])

class move:
    def POST(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        source = web.input().source_zone
        destination = web.input().target_zone
        card_id = uuid.UUID(web.input().uuid)
        from_top = bool(web.input().get("from_top", False))
        num_down = int(web.input().get("num_down", 0))
        if not main.user_deck_managers[user_id].move(source, destination, card_id, from_top, num_down):
            raise web.BadRequest("Move failed, probably because that card isn't in the source zone.")
        raise web.seeother("/play")

class tuck:
    def GET(self):
        user_id = web.cookies().get(ID_COOKIE_NAME)
        card_id = uuid.UUID(web.input().uuid)
        return render.tuck(main.user_deck_managers[user_id].card_for_uuid(card_id))


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
