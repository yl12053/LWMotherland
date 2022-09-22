import flask
from blueprint import apps
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy()
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lwmotherland%40lwmland:LWm3therland@lwmland.mysql.database.azure.com"
db.init_app(app)


@app.route("/assets/<path:path>")
def assets(path):
    return flask.send_from_directory("assets", path)


for x in apps:
    app.register_blueprint(x)

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
