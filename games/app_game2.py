from flask import Blueprint
import flask
from flask import make_response
from flask_login import current_user, login_required
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
import binascii
import random

initialized = False

app = Blueprint('app_game2', __name__)

game2key = {}
hexmap = {}
allowhex = []

initialized = True
print("[Worker 2] Disabled.")

max_question = 10


@app.route("/dynamic/g2dynam.js")
@login_required
def gheader():
  hx = flask.request.args.get("hx")
  if hx not in allowhex:
    flask.abort(403)
  allowhex.remove(hx)
  p1, p2 = tuple(game2key[hx][0][1])
  rtemplate = Environment(loader=BaseLoader).from_string(
    open(
      f"dynamic_file/Game2{('' if current_app.config['T_DEBUG'] else '_Obfuscation')}.js",
      encoding="utf-8").read())
  return rtemplate.render(hx=hx, px=hex(p1), py=hex(p2))


@app.route("/apis/game2/fetch", methods=['POST'])
@login_required
def fet():
  hx = flask.request.form.get("hx")
  if hx not in game2key.keys() or (game2key[hx][2] - time.time() > 600):
    flask.abort(403)
  if game2key[hx][1] is None:
    flask.abort(403)
  question_data = Model.Game2Q.query.filter_by(Random=1).all()
  retD = []
  nqd = Model.Game2Q.query.filter_by(Random=0).all()
  random.shuffle(nqd)
  for x in question_data:
    retD.append([x.id, x.Question, x.Options, x.Correct])
  np = 0
  while len(retD) < max_question:
    x = nqd[np]
    retD.append([x.id, x.Question, x.Options, x.Correct])
    np += 1
  retst = json.dumps(retD)
  bytst = retst.encode("utf-8")
  padst = bytst + ((AES.block_size - (len(bytst) % AES.block_size)) *
                   chr(AES.block_size - len(bytst) % AES.block_size)).encode()
  cipher = AES.new(game2key[hx][1][0], AES.MODE_CBC, game2key[hx][1][1])
  print("IV =", binascii.hexlify(game2key[hx][1][1]))
  game2key[hx][1][1] = hashlib.sha256(game2key[hx][1][1]).digest()[:16]
  print("IV ->", binascii.hexlify(game2key[hx][1][1]))
  senst = cipher.encrypt(padst)
  b64st = base64.b64encode(senst)
  return b64st.decode()


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


@app.route("/apis/game2/hand_in", methods=["POST"])
@login_required
def hand():
  hx = flask.request.form.get("hx")
  if hx not in game2key.keys() or (game2key[hx][2] - time.time() > 600):
    flask.abort(403)
  if game2key[hx][1] is None:
    flask.abort(403)
  stud_input_b = flask.request.form.get("raw")
  try:
    stud_input_enc = base64.b64decode(stud_input_b.encode())
  except:
    flask.abort(400)
  cipher = AES.new(game2key[hx][1][0], AES.MODE_CBC, game2key[hx][1][1])
  decs = cipher.decrypt(stud_input_enc)
  if len(decs) == 0:
    flask.abort(403)
  last_bit = decs[-1]
  if (last_bit > 15 or len(list(set(decs[-last_bit:]))) > 1):
    flask.abort(403)
  stud_input_raw = decs[:-last_bit]
  try:
    stud_input = json.loads(stud_input_raw.decode())
  except:
    print("Decode failed")
    print(stud_input_raw)
    flask.abort(400)
  question_data = Model.Game2Q.query.all()
  marks = 0
  for question in range(len(stud_input)):
    if (stud_input[question] is not None):
      for n in range(len(stud_input[question])):
        if stud_input[question][n] == question_data[question].Correct[n]:
          marks += 10
  t = Model.Game2Details.query.filter_by(id=current_user.id).first()
  if t is None:
    new = Model.Game2Details(current_user.id, stud_input, marks)
    Model.self_db.session.add(new)
  else:
    t.details = stud_input
    t.marks = marks
  mdf = Model.player_position.query.filter_by(id=current_user.id).first()
  if (mdf.preventRedone < 2):
    mdf.preventRedone = 2
  Model.self_db.session.commit()
  return "OK"


@app.route("/Game2")
@login_required
def leader():
  mdf = Model.player_position.query.filter_by(id=current_user.id).first()
  if mdf is not None:
    if mdf.preventRedone != 1:
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
      flask.render_template(
        "game/Game2.html",
        cg=("false" if flask.request.args.get("cg") == "0" else "true"),
        hx=hexs,
        len=len,
      ))
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
      flask.render_template(
        "game/Game2.html",
        cg=f,
        hx=hexs,
        len=len,
      ))
    return resp
