import bottle
from mirrorpy.plugin import Plugin


class Server(bottle.Bottle):
    def __init__(self):
        bottle.Bottle.__init__(self)
        self.route("/", "GET", self.index)
        self.route("/<filename:re:.*\.(css|js|eot|svg|ttf|woff|woff2)>", "GET", self.static)

    def register_plugin(self, plugin: Plugin, path: str):
        self.route(path, "GET", plugin.get)

    def index(self):
        with open("website/index.html") as f:
            return f.read()

    def static(self, filename):
        return bottle.static_file(filename, root='website')


