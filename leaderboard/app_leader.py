from flask import Blueprint
import flask
from sqlalchemy import distinct
from sqlalchemy import func
from models.app_db import Model

app = Blueprint('app_leader', __name__)


@app.route("/leaderboard")
def leader():
  return flask.render_template("leaderboard/leaderboard.html")


@app.route("/lbs")
def p():
  groups = Model.self_db.session.query(Model.Users.grp).distinct().all()
  ppls = []
  for x in groups:
    ppls.append(Model.Users.query.filter_by(grp=x[0]).first())
  #print(ppls)
  ppl_dict = {x.id: x.grp for x in ppls}
  return_list = []
  for x in ppl_dict.keys():
    ogub = ppl_dict[x]
    return_sub = [ppl_dict[x]]
    mark = 130
    g1b = Model.Game1Bypass.query.filter_by(id=x).first()
    if g1b is not None:
      mark -= len(g1b.tipsGiven) * 10
    g1 = Model.Game1Details.query.filter_by(id=x).first()
    if g1b is not None:
      mark += g1.correctCountGame1 * 10
    addi = Model.self_db.session.query(func.sum(
      Model.additional_mark.mark)).filter(
        Model.additional_mark.group == ogub).first()[0]
    mark += (0 if addi is None else int(addi))
    return_sub.append(mark)
    return_list.append(return_sub)
  return flask.jsonify(return_list)
