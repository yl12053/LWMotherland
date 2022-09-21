import flask
from blueprint import apps

app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/assets/<path:path>")
def assets(path):
    return flask.send_from_directory("assets", path)


for x in apps:
    app.register_blueprint(x)

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
