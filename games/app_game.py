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
import random

app = Blueprint('app_game', __name__)

game1key = {}
hexmap = {}
allowhex = []

mc_number = 15
"""
with current_app.app_context():
  if mc_number > Model.self_db.Game1Q.query.count():
    mc_number = Model.self_db.Game1Q.query.count()
    print(
      "[Game 1] WARNING: Maximum number of MC is larger than the number of question in database."
    )
  if mc_number < Model.self_db.Game1Q.query.filter_by(Random=0).count():
    mc_number = Model.self_db.Game1Q.query.filter_by(Random=0).count()
    print(
      "[Game 1] WARNING: Maximum number of MC is smaller than the number of the question need to be shown in database."
    )
"""


@app.route("/dynamic/g1dynam.js")
@login_required
def gheader():
  hx = flask.request.args.get("hx")
  if hx not in allowhex:
    flask.abort(403)
  allowhex.remove(hx)
  p1, p2 = tuple(game1key[hx][0][1])
  rtemplate = Environment(loader=BaseLoader).from_string(
    open("dynamic_file/Game1%s.js" %
         ("" if current_app.config["T_DEBUG"] else "_Obfuscation")).read())
  return rtemplate.render(hx=hx, px=hex(p1), py=hex(p2))


@app.route("/apis/game1/ecdhe", methods=['POST'])
@login_required
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


@app.route("/apis/game1/update", methods=["POST"])
@login_required
def updGame1():

  def timeCompansation(t):
    if 10 <= t <= 20:
      return 2
    elif 20 < t <= 30:
      return 5
    elif 30 < t:
      return 10
    else:
      return 0

  payload = flask.request.form.get("payload")
  try:
    p = base64.b64decode(payload.encode())
    if (len(p) == 0) or len(p) % 16:
      flask.abort(400)
  except:
    flask.abort(400)
  hx = hexmap[current_user.id]
  del hexmap[current_user.id]
  cipher = AES.new(game1key[hx][1][0], AES.MODE_CBC, game1key[hx][1][1])
  decd = cipher.decrypt(p)
  if len(decd) == 0:
    flask.abort(403)
  last_bit = decd[-1]
  if (last_bit > 15 or len(list(set(decd[-last_bit:]))) > 1):
    flask.abort(403)
  realdata = decd[:-last_bit]
  try:
    readable = json.loads(realdata.decode())
  except:
    flask.abort(403)
  cct = readable["corrCount"]
  wrt = readable["wrongCount"]
  tleft = readable["timeLeft"]
  clientCalculated = readable["mark"]
  if (clientCalculated != cct + timeCompansation(tleft)):
    return "Fake Data"
  mod = Model.Game1Details.query.filter_by(id=current_user.id).first()
  if mod is None:
    mod = Model.Game1Details(current_user.id, cct, wrt, tleft,
                             clientCalculated)
    Model.self_db.session.add(mod)
  else:
    mod.correctCountGame1 = cct
    mod.wrongCountGame1 = wrt
    mod.timeLeftGame1 = tleft
    mod.mark1 = clientCalculated
  mdf = Model.player_position.query.filter_by(id=current_user.id).first()
  if (mdf.preventRedone < 1):
    mdf.preventRedone = 1
  Model.self_db.session.commit()
  return "OK"


@app.route("/apis/game1/fetch_q", methods=['POST'])
@login_required
def ques():
  hx = flask.request.form.get("hx")
  if hx not in game1key.keys() or (game1key[hx][2] - time.time() > 600):
    flask.abort(403)
  if game1key[hx][1] is None:
    flask.abort(403)
  qs = Model.Game1Q.query.filter_by(Random=1).all()
  notneed = Model.Game1Q.query.filter_by(Random=0).all()
  shuffled_notneed = random.shuffle(notneed)
  rtd = []
  for x in qs:
    rtd.append([
      x.Id, x.Question, x.Option1, x.Option2, x.Option3, x.Option4, x.Answer,
      x.Random
    ])
  n = 0
  while len(rtd) < mc_number:
    x = shuffled_notneed
    rtd.append([
      x.Id, x.Question, x.Option1, x.Option2, x.Option3, x.Option4, x.Answer,
      x.Random
    ])
    n += 1
  encStr = json.dumps(rtd)
  byteStr = encStr.encode("utf8")
  padStr = byteStr + (
    (AES.block_size - (len(byteStr) % AES.block_size)) *
    chr(AES.block_size - len(byteStr) % AES.block_size)).encode()
  cipher = AES.new(game1key[hx][1][0], AES.MODE_CBC, game1key[hx][1][1])
  game1key[hx][1][1] = hashlib.sha256(game1key[hx][1][1]).digest()[:16]
  doneStr = cipher.encrypt(padStr)
  b64Str = base64.b64encode(doneStr)
  return b64Str.decode()


@app.route("/apis/game1/keep_key_alive", methods=["POST"])
@login_required
def kalive():
  hx = flask.request.form.get("hx")
  if hx not in game1key.keys() or (game1key[hx][2] - time.time() > 600):
    flask.abort(403)
  game1key[hx][2] = time.time()
  return "OK"


@app.route("/Game1")
@login_required
def leader():
  mss = Model.Game1Bypass.query.filter_by(id=current_user.id).first()
  if (not (mss and mss.passed)):
    return flask.redirect("/GameB1")
    pass
  mdf = Model.player_position.query.filter_by(id=current_user.id).first()
  if mdf is not None:
    if mdf.preventRedone >= 2:
      return flask.redirect("/map")
  hexs = uuid.uuid4().hex
  while hexs in game1key.keys() and game1key[hexs][2] - time.time() <= 600:
    hexs = uuid.uuid4().hex
  privkey, pubkey = ecdhe.make_keypair()
  game1key[hexs] = [[privkey, pubkey], None, time.time()]
  allowhex.append(hexs)
  hexmap[current_user.id] = hexs
  if flask.request.args.get("cg"):
    resp = make_response(
      flask.render_template(
        "game/Game1.html",
        cg=("false" if flask.request.args.get("cg") == "0" else "true"),
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
