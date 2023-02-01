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
from jinja2 import Environment, BaseLoader, Template
from flask import current_app
import threading

initialized = False

app = Blueprint('app_game2', __name__)

game2key = {}
hexmap = {}
allowhex = []
question_datas = []

def thread_caching():
    global question_datas, initialized
    if not getattr(Model, "_initialized", False):
        print("[Worker 2] Waiting for model initialization")
        while not getattr(Model, "_initialized", False):
            pass
    with Model.curr_app.app_context():
        print("[Worker 2] Caching Game 2 Question")
        question_data = Model.Game2Q.query.all()
        print("[Worker 2] Preprocessing Game 2...")
        for x in question_data:
            html = Template("{{x.id}}.  " + x.Question)
            replace_dict = {"x": x}
            for y in range(1, len(x.Correct) + 1):
                replace_id = f"replace_{y}"
                replace_content = Template(
                    "<span class='blank'><span class='text_container' id='q{{x.id}}_{{y}}'>&nbsp;</span><span class='choice_cloud'>{% for i in range(len(x.Options[y-1])) %}<span class='choice'>{{x.Options[y-1][i]}}</span>{% endfor -%}</span></span>"
                ).render(x=x, y=y, len=len)
                replace_dict[replace_id] = replace_content
            replace_result = html.render(**replace_dict)
            question_datas.append(replace_result)
        print("[Worker 2] Caching finished.")
        initialized = True
threading.Thread(target=thread_caching, daemon=True).start()

@app.route("/dynamic/g2dynam.js")
@login_required
def gheader():
    hx = flask.request.args.get("hx")
    if hx not in allowhex:
        flask.abort(403)
    allowhex.remove(hx)
    p1, p2 = tuple(game2key[hx][0][1])
    rtemplate = Environment(loader=BaseLoader).from_string(
        open("dynamic_file/Game2%s.js" %
             ("" if current_app.config["T_DEBUG"] else "_Obfuscation")).read())
    return rtemplate.render(hx=hx, px=hex(p1), py=hex(p2))


@app.route("/apis/game2/ecdhe", methods=['POST'])
@login_required
def ecd():
    hx = flask.request.form.get("hx")
    if hx not in game2key.keys() or (game2key[hx][2] - time.time() > 600):
        flask.abort(403)
    pubx = int(flask.request.form.get("px"))
    puby = int(flask.request.form.get("py"))
    priv = game2key[hx][0][0]
    rec = ecdhe.key_exchange(priv, (pubx, puby))
    game2key[hx][1] = [
        rec[0].to_bytes(32, 'big'), rec[1].to_bytes(32, 'big')[:16]
    ]
    return "OK"


@app.route("/apis/game2/keep_key_alive", methods=["POST"])
@login_required
def kalive():
    hx = flask.request.form.get("hx")
    if hx not in game2key.keys() or (game2key[hx][2] - time.time() > 600):
        flask.abort(403)
    game2key[hx][2] = time.time()
    return "OK"


@app.route("/Game2")
@login_required
def leader():
    mdf = Model.player_position.query.filter_by(id=current_user.id).first()
    if mdf is not None:
        if mdf.preventRedone >= 2:
            return flask.redirect("/map")
    hexs = uuid.uuid4().hex
    while hexs in game2key.keys() and game2key[hexs][2] - time.time() <= 600:
        hexs = uuid.uuid4().hex
    privkey, pubkey = ecdhe.make_keypair()
    game2key[hexs] = [[privkey, pubkey], None, time.time()]
    allowhex.append(hexs)
    hexmap[current_user.id] = hexs
    if flask.request.args.get("cg"):
        resp = make_response(
            flask.render_template("game/Game2.html",
                                  cg=("false" if flask.request.args.get("cg")
                                      == "0" else "true"),
                                  hx=hexs, len=len, question_datas=question_datas))
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
            flask.render_template("game/Game2.html", cg=f, hx=hexs, len=len, question_datas=question_datas))
        return resp
