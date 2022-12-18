import uuid

import web
import main

ID_COOKIE_NAME = "uuid"

urls = ("/", "index",
        "/new", "new",
        "/play", "play")
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



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
