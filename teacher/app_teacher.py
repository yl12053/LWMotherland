from flask import Blueprint
import flask
import json
from models.app_db import Model
import itertools
from sqlalchemy import text

app = Blueprint('app_teacher', __name__)


@app.route("/tmans")
def tman():
  return flask.render_template("PaperSend.html",
                               data=json.dumps(Model.handle),
                               names=json.dumps(Model.nameMap))


@app.route("/dbm/data")
def database():
  return flask.render_template("database/data.html")


@app.route("/dbm/readTable")
def getTable():
  tabdata = Model.self_db.engine.execute("show tables")
  lst = list(itertools.chain.from_iterable(tabdata.all()))
  return flask.jsonify(lst)


@app.route("/dbm/getDetails", methods=["POST"])
def getDetails():
  dts = flask.request.form.get("table")
  try:
    detail = list(map(list, Model.self_db.engine.execute("describe `%s`"%(dts)).all()))
    cnt = Model.self_db.engine.execute("select count(*) from `%s`"%dts).first()[0]
    return flask.jsonify({"Error": False, "Column": detail, "Count": cnt})
  except Exception as e:
    return flask.jsonify({
      "Error": True,
      "Code": e.orig.args[0],
      "Statement": e.orig.args[1]
    })

@app.route("/dbm/getRecords", methods=["POST"])
def getRecords():
  dts = flask.request.form.get("table")
  off = int(flask.request.form.get("offset"))
  lim = int(flask.request.form.get("limit"))
  try:
    return flask.jsonify({"Error": False, "Result": list(map(list, Model.self_db.engine.execute("select * from `%s` limit %d offset %d"%(dts, lim, off)).all()))})
  except Exception as e:
    return flask.jsonify({
      "Error": True,
      "Code": e.orig.args[0],
      "Statement": e.orig.args[1]
    })