from flask import Blueprint
import flask
import json
from models.app_db import Model

app = Blueprint('app_teacher', __name__)


@app.route("/tmans")
def tman():
    return flask.render_template("PaperSend.html",
                                 data=json.dumps(Model.handle),
                                 names=json.dumps(Model.nameMap))
