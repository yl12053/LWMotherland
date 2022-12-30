from flask import Blueprint
import flask
from flask import make_response
from flask_login import current_user
from models.app_db import Model
from modules import ecdhe
import time
import json
import uuid
import hashlib
import base64
from Crypto.Cipher import AES
from jinja2 import Environment, BaseLoader
from flask import current_app

app = Blueprint('app_game3', __name__)

game3key = {}
hexmap = {}
allowhex = []


@app.route("/dynamic/g3dynam.js")
def gheader():
    hx = flask.request.args.get("hx")
    if hx not in allowhex:
        flask.abort(403)
    allowhex.remove(hx)
    p1, p2 = tuple(game3key[hx][0][1])
    rtemplate = Environment(loader=BaseLoader).from_string(
        open("dynamic_file/Game3%s.js" %
             ("" if current_app.config["T_DEBUG"] else "_Obfuscation")).read())
    return rtemplate.render(hx=hx, px=hex(p1), py=hex(p2))


@app.route("/apis/game3/ecdhe", methods=['POST'])
def ecd():
    hx = flask.request.form.get("hx")
    if hx not in game3key.keys() or (game3key[hx][2] - time.time() > 600):
        flask.abort(403)
    pubx = int(flask.request.form.get("px"))
    puby = int(flask.request.form.get("py"))
    priv = game3key[hx][0][0]
    rec = ecdhe.key_exchange(priv, (pubx, puby))
    game3key[hx][1] = [
        rec[0].to_bytes(32, 'big'), rec[1].to_bytes(32, 'big')[:16]
    ]
    return "OK"


@app.route("/apis/game3/keep_key_alive", methods=["POST"])
def kalive():
    hx = flask.request.form.get("hx")
    if hx not in game3key.keys() or (game3key[hx][2] - time.time() > 600):
        flask.abort(403)
    game3key[hx][2] = time.time()
    return "OK"


@app.route("/Game3")
def leader():
    mdf = Model.player_position.query.filter_by(id=current_user.id).first()
    if mdf is not None:
        if mdf.preventRedone >= 2:
            return flask.redirect("/map")
    hexs = uuid.uuid4().hex
    while hexs in game3key.keys() and game3key[hexs][2] - time.time() <= 600:
        hexs = uuid.uuid4().hex
    privkey, pubkey = ecdhe.make_keypair()
    game3key[hexs] = [[privkey, pubkey], None, time.time()]
    allowhex.append(hexs)
    hexmap[current_user.id] = hexs
    if flask.request.args.get("cg"):
        resp = make_response(
            flask.render_template("game/Game3.html",
                                  cg=("false" if flask.request.args.get("cg")
                                      == "0" else "true"),
                                  hx=hexs))
        return resp
    else:
        mdf = Model.player_position.query.filter_by(id=current_user.id).first()
        if mdf is None:
            mdf = Model.player_position(current_user.id, 2, -1, -1, 0)
            Model.self_db.session.add(mdf)
        if mdf.reserved == 0:
            mdf.reserved = 1
            f = "true"
        else:
            f = "false"
        Model.self_db.session.commit()
        resp = make_response(
            flask.render_template("game/Game3.html", cg=f, hx=hexs))
        return resp
