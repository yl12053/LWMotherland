from flask import Blueprint
import flask
from flask import make_response
from flask_login import current_user
from models.app_db import Model
from modules import ecdhe
import time

app = Blueprint('app_game3', __name__)


@app.route("/apis/game3/notify")
def notify():
    if current_user.id not in Model.dataCompleted:
        if current_user.id not in (Model.nameMap):
            Model.nameMap[current_user.id] = Model.Users.query.filter_by(
                id=current_user.id).first().used_name
        Model.dataCompleted.add(current_user.id)
        dti = (
            time.time() * 1000,
            current_user.id,
        )
        Model.handle.append(dti)
        Model.handler(*dti)
    return "OK"


@app.route("/Game3")
def leader():
    mdf = Model.player_position.query.filter_by(id=current_user.id).first()
    if mdf is not None:
        if mdf.preventRedone < 2:
            return flask.redirect("/map")
    privkey, pubkey = ecdhe.make_keypair()
    cg = "true"
    if mdf is not None:
        if mdf.preventRedone == 3:
            cg = "false"
    if mdf is None:
        mdf = Model.player_position(current_user.id, 3, -1, -1, 0)
        Model.self_db.session.add(mdf)
    mdf.preventRedone = 3
    Model.self_db.session.commit()
    resp = make_response(flask.render_template("game/Game3.html", cg=cg))
    return resp
