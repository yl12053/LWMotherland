from flask import Blueprint
import flask
from flask import make_response
from flask_login import current_user, login_required
from models.app_db import Model
import time, json, random

app = Blueprint('app_gameb1', __name__)


@login_required
@app.route("/apis/GameB1/checkAnswer", methods=["POST"])
def check():
  try:
    studAns = list(map(int, json.loads(flask.request.form.get("ans"))))
  except:
    return flask.jsonify({"Error": -1})
  if len(studAns) != 8:
    return flask.jsonify({"Error": 1})
  modelAns = Model.Game1BQ.query.first()
  ansW = modelAns.WrongIndex
  allwrong = []
  for n in ansW:
    if n in studAns:
      allwrong.append(n)
  if len(allwrong):
    studModel = Model.Game1Bypass.query.filter_by(id=current_user.id).first()
    ranc = random.choice(allwrong)
    if (studModel is None):
      studModel = Model.Game1Bypass(current_user.id, [ranc], 0)
      Model.self_db.session.add(studModel)
    else:
      studModel.tipsGiven = studModel.tipsGiven + [ranc]
    Model.self_db.session.commit()
    return flask.jsonify({"Error": 2, "Tips": ranc})
  studModel = Model.Game1Bypass.query.filter_by(id=current_user.id).first()
  if (studModel is None):
    studModel = Model.Game1Bypass(current_user.id, [], 1)
    Model.self_db.session.add(studModel)
  studModel.passed = 1
  Model.self_db.session.commit()
  return flask.jsonify({"Error": 0})


@login_required
@app.route("/GameB1")
def gameb1():
  if (Model.Game1Bypass.query.filter_by(id=current_user.id, passed=1).count()):
    return flask.redirect("/Game1?cg=1", 301)
  qM = Model.Game1BQ.query.first()
  allS = json.dumps(qM.All)
  usd = Model.Game1Bypass.query.filter_by(id=current_user.id).first()
  if usd:
    ws = usd.tipsGiven
    if ws is None:
      ws = []
    rws = [qM.All[x] for x in range(len(qM.All)) if x not in ws]
  else:
    rws = qM.All
  rwp = json.dumps(rws)
  resp = make_response(
    flask.render_template("game/Gameb1.html", listAll=allS, listSel=rwp))
  return resp


def tipsGive():
  pers = Model.Game1Bypass.query.filter_by(id=current_user.id).first()
  allerr = Model.Game1BQ.query.first().WrongIndex
  if (pers is None):
    allow = allerr
  else:
    allow = [x for x in allerr if x not in pers.tipsGiven]
  removeItem = random.choice(allow)
  if (pers is None):
    pers = Model.Game1Bypass(current_user.id, [removeItem], 0)
    Model.self_db.session.add(pers)
  else:
    pers.tipsGiven = pers.tipsGiven + [removeItem]
  Model.self_db.session.commit()
  return str(removeItem)
