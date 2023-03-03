import flask
from flask_cors import cross_origin
import json
from flask_socketio import SocketIO, join_room, emit
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from models.app_db import init, Model
from blueprint import apps
from flask_login import LoginManager, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed
import os
import sys
import hashlib

app = flask.Flask(__name__)
principals = Principal(app)
app.secret_key = "sctkey"
app.config["static_url_path"] = "assets"
app.config["static_folder"] = 'assets'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'homepage'
socketio = SocketIO(app)

if len(sys.argv) and sys.argv[-1] == "debug":
  app.config["T_DEBUG"] = True
else:
  app.config["T_DEBUG"] = False


@login_manager.user_loader
def user_loader(usr):
  user = Model.Users
  return user.query.get(int(usr))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
  identity.user = current_user
  if hasattr(current_user, 'id'):
    identity.provides.add(UserNeed(current_user.id))
  if hasattr(current_user, 'role'):
    if current_user.role:
      for role in current_user.role:
        identity.provides.add(RoleNeed(role))


@app.context_processor
def cache_busters():
  return {
    'assets':
    'https://raw.githubusercontent.com/yl12053/LWMotherland/Dev/assets',
    "local_assets": "/assets"
  }


@app.after_request
def add_header(r):
  if hasattr(r, 'ext_cac'):
    return r
  else:
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
  return r


app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy()
app.config[
  "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://lwmotherland:lwmotherland@db4free.net/lwmotherland"
init(db, app)


@app.route("/assets/<path:path>")
@cross_origin()
def assets(path):
  rtv = flask.send_from_directory(
    "assets",
    path,
    conditional=False,
    as_attachment=False,
    download_name=None,
  )
  rtv.headers['Cache-Control'] = "no-cache, must-revalidate"
  rtv.make_conditional(flask.request)
  rtv.ext_cac = True
  return rtv


@app.route("/google95a4c2e4ac08c0ae.html", methods=["GET", "POST"])
def google_verification_verify():
  return open("static_root/google95a4c2e4ac08c0ae.html").read()


if app.config["T_DEBUG"]:

  @app.route("/")
  def root():
    return open("index.html", "r").read()

  @app.route("/lb")
  def leaderboard():
    return open("view.html", "r").read()

  @app.route("/home")
  def homepage():
    return render_template("homepage/home.html")

else:

  @app.route("/")
  def root():
    return render_template("homepage/home.html")


@app.route("/map")
@login_required
def map():
  mdf = Model.player_position.query.filter_by(id=current_user.id).first()
  if mdf is not None:
    rerr = mdf.preventRedone
  else:
    rerr = 0
  return render_template("map/map.html",
                         asset_file="/assets/video/newmap.mp4",
                         type_asset="video",
                         width="2020",
                         height="1520",
                         rerr=str(rerr))


for x in apps:
  app.register_blueprint(x)


@app.route("/lbs")
def p():
  tabd = Model.self_db.engine.execute(
    "select concat(grps, ' (', mid(sec_to_time(avg(game1tl)), 4, 8), ')'), avg(total) as 'avgTotal' from (select Auth.grp as 'grps', Auth.subindex as 'sid', sum(ifnull(Game1Details.timeLeftGame1, 0)) as 'game1tl', sum(if(Game1Bypass.passed = 0 or Game1Bypass.passed is null, 0, 130 - if(Game1Bypass.tipsGiven is NULL, 0, JSON_LENGTH(Game1Bypass.tipsGiven)*10)) + ifnull(Game1Details.correctCountGame1*10 + Game1Details.timeBonus, 0) + ifnull(Game2Details.marks, 0)) as 'total' from Game1BQ, (((Auth left join Game1Details on Auth.id=Game1Details.id) left join Game2Details on Auth.id=Game2Details.id) left join Game1Bypass on Auth.id=Game1Bypass.id) group by Auth.grp, Auth.subindex) as firstResult group by grps order by avgTotal desc, avg(game1tl) desc, grps asc;"
  ).all()
  return flask.jsonify([[x[0], float(x[1])] for x in tabd])


@app.route("/<path:path>")
def asroot(path):
  return flask.send_from_directory("As_Root",
                                   path,
                                   conditional=False,
                                   as_attachment=False,
                                   download_name=None)


@app.route(app.static_url_path + '/' + '<path:path>' + ".ts")
def jsonl_mime_type(path):
  return flask.send_from_directory(directory=app.static_folder,
                                   path=path + ".ts",
                                   mimetype="text/javascript")


def hand(t, u):
  with app.app_context():
    usr = Model.Users.query.filter_by(id=u).first()
    name = usr.used_name
  socketio.emit('sdone', {"name": name, "time": t, "id": u}, to='manag')


@socketio.on('join')
def j(d):
  join_room("manag")
  print("[SocketIO] Teacher emitted event join")
  emit('joined', {})


@socketio.on('connect')
def onCon(conn):
  print("[SocketIO] Teacher joined")
  emit('ableToJoin', {})


Model.handler = hand

print("[Main] Runway Clear!")
if __name__ == "__main__":
  app.run("0.0.0.0", 5000)
