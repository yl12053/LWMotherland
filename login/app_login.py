from flask import Blueprint, redirect, request
from flask_login import UserMixin, login_user, current_user, logout_user
from models.app_db import Model
import flask, os, hashlib, json, requests
from urllib import parse

app = Blueprint('app_login', __name__)
logining_user = {}
client_id = json.load(open("rjson.json"))["web"]["client_id"]


@app.route("/login")
def login_page():
    return """
    <form id='fms' method='POST' action='/login_redr' style="display: None">
      <input name='origin' id='origin'>
      <input name='jump' id='jump'>
    </form>
    <script>
      var queryString = window.location.search;
      var urlParams = new URLSearchParams(queryString);
      document.getElementById('origin').value = window.location.origin;
      document.getElementById('jump').value = urlParams.get('jump');
      if (document.getElementById('jump').value == null){
        document.getElementById('jump').value = '';
      }
      document.getElementById('fms').submit();
    </script>
    """


@app.route("/login_redr", methods=["POST"])
def redr():
    if request.form.get("origin") is None:
        return "None"
    ptoken = hashlib.sha256(os.urandom(32)).hexdigest()
    while ptoken in logining_user.keys():
        ptoken = hashlib.sha256(os.urandom(32)).hexdigest()
    logining_user[ptoken] = request.form.get("jump")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/userinfo.email%20https%3A//www.googleapis.com/auth/userinfo.profile&response_type=token&state={ptoken}&redirect_uri={parse.quote(request.form.get('origin')+'/login_retr')}&client_id={parse.quote(client_id)}",
        301)


@app.route("/login_retr")
def retr():
    return """
    <script>
      window.location = window.location.origin+'/login_repr?'+location.hash.slice(1);
    </script>
    """


@app.route('/login_repr')
def repr():
    if request.args.get("error") is not None:
        return request.args.get("error")
    if request.args.get("state") is None:
        return "No state provided."
    if request.args.get("state") not in logining_user:
        return "No such state"
    jmp = logining_user[request.args.get("state")]
    del logining_user[request.args.get("state")]
    j = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                     headers={
                         "Authorization":
                         "Bearer " + request.args.get("access_token")
                     }).json()
    if j.get("hd") != "lamwoo.edu.hk":
        return "Not a internal member"
    gname = j['given_name']
    clas = gname.split()[0][1:]
    cno = int(gname.split()[1])
    uqur = Model.Users.query.filter_by(clas=clas, cno=cno).first()

    if uqur is None:
        return "Failed: Not registered in Database"
    if uqur.used_name != j['name']:
        uqur.used_name = j['name']
        Model.self_db.session.commit()
    login_user(uqur)
    if jmp != '':
        return redirect(jmp, 301)
    return "Login successful."


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        if request.args.get("jump"):
            return redirect(request.args.get("jump"))
        return "Done"
    else:
        if request.args.get("jump"):
            return redirect(request.args.get("jump"))
        return "Not logined"


@app.route("/login_test")
def test():
    if current_user is None:
        return "Not login"
    else:
        return "Class: %s<br>Class Number: %d" % (current_user.clas,
                                                  current_user.cno)
