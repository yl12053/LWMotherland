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

app = Blueprint('app_game', __name__)

game1key = {}
allowhex = []


@app.route("/dynamic/g1dynam.js")
def gheader():
    hx = flask.request.args.get("hx")
    if hx not in allowhex:
        flask.abort(403)
    allowhex.remove(hx)
    p1, p2 = tuple(game1key[hx][0][1])
    rtemplate = Environment(loader=BaseLoader).from_string(
        open("dynamic_file/Game1_Obfuscation.js").read())
    return rtemplate.render(hx=hx, px=hex(p1), py=hex(p2))


@app.route("/apis/game1/ecdhe", methods=['POST'])
def ecd():
    hx = flask.request.form.get("hx")
    if hx not in game1key.keys() or (game1key[hx][2] - time.time() > 600):
        flask.abort(403)
    pubx = int(flask.request.form.get("px"))
    puby = int(flask.request.form.get("py"))
    priv = game1key[hx][0][0]
    rec = ecdhe.key_exchange(priv, (pubx, puby))
    game1key[hx][1] = [
        rec[0].to_bytes(32, 'big'), rec[1].to_bytes(32, 'big')[:16]
    ]
    return "OK"


@app.route("/apis/game1/fetch_q", methods=['POST'])
def ques():
    hx = flask.request.form.get("hx")
    if hx not in game1key.keys() or (game1key[hx][2] - time.time() > 600):
        flask.abort(403)
    if game1key[hx][1] is None:
        flask.abort(403)
    qs = Model.Game1Q.query.all()
    rtd = []
    for x in qs:
        rtd.append([
            x.Id, x.Question, x.Option1, x.Option2, x.Option3, x.Option4,
            x.Answer, x.Random
        ])
    encStr = json.dumps(rtd)
    byteStr = encStr.encode("utf8")
    padStr = byteStr + (
        (AES.block_size - (len(byteStr) % AES.block_size)) *
        chr(AES.block_size - len(byteStr) % AES.block_size)).encode()
    cipher = AES.new(game1key[hx][1][0], AES.MODE_CBC, game1key[hx][1][1])
    doneStr = cipher.encrypt(padStr)
    b64Str = base64.b64encode(doneStr)
    return b64Str.decode()


@app.route("/apis/game1/keep_key_alive", methods=["POST"])
def kalive():
    hx = flask.request.form.get("hx")
    if hx not in game1key.keys() or (game1key[hx][2] - time.time() > 600):
        flask.abort(403)
    game1key[hx][2] = time.time()
    return "OK"


@app.route("/Game1")
def leader():
    hexs = uuid.uuid4().hex
    while hexs in game1key.keys() and game1key[hexs][2] - time.time() <= 600:
        hexs = uuid.uuid4().hex
    privkey, pubkey = ecdhe.make_keypair()
    game1key[hexs] = [[privkey, pubkey], None, time.time()]
    allowhex.append(hexs)
    if flask.request.args.get("cg"):
        resp = make_response(
            flask.render_template("game/Game1.html",
                                  cg=("false" if flask.request.args.get("cg")
                                      == "0" else "true"),
                                  hx=hexs))
        return resp
    else:
        mdf = Model.player_position.query.filter_by(id=current_user.id).first()
        if mdf is None:
            mdf = Model.player_position(current_user.id, 1, -1, -1, 0)
            Model.self_db.session.add(mdf)
        if mdf.reserved == 0:
            mdf.reserved = 1
            f = "true"
        else:
            f = "false"
        Model.self_db.session.commit()
        resp = make_response(
            flask.render_template("game/Game1.html", cg=f, hx=hexs))
        return resp
