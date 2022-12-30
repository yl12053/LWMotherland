from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, current_user
from flask import request
import threading


class Model:
    pass


def init(db, app):
    classes(db)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/changeLoc", methods=["POST"])
    @login_required
    def cloc():
        q = Model.player_position.query.filter_by(id=current_user.id).first()
        if q is None:
            q = Model.player_position(current_user.id,
                                      int(request.form.get("dim")),
                                      int(request.form.get("x")),
                                      int(request.form.get("y")),
                                      request.form.get("reserved"),
                                      0)
            db.session.add(q)
        else:
            q.dim = int(request.form.get("dim"))
            q.x = int(request.form.get("x"))
            q.y = int(request.form.get("y"))
            q.reserved = request.form.get("reserved")
        db.session.commit()
        return "Success"


def classes(db):

    class Users(db.Model, UserMixin):
        __tablename__ = "Auth"
        id = db.Column(db.Integer, primary_key=True)
        clas = db.Column(db.VARCHAR(2))
        cno = db.Column(db.Integer)
        grp = db.Column(db.Integer)
        used_name = db.Column(db.VARCHAR(255))

        def __init__(self, id, clas, cno, grp, name):
            self.id = id
            self.clas = clas
            self.cno = cno
            self.grp = grp
            self.used_name = name

    class player_position(db.Model):
        __tablename__ = "player_position"
        id = db.Column(db.Integer, primary_key=True)
        dim = db.Column(db.Integer)
        x = db.Column(db.Integer)
        y = db.Column(db.Integer)
        reserved = db.Column(db.Integer)
        preventRedone = db.Column(db.Integer)

        def __init__(self, id, dim, x, y, reserved, preventRedone=0):
            if preventRedone < 0:
                preventRedone = 0
            self.id = id
            self.dim = dim
            self.x = x
            self.y = y
            self.reserved = reserved
            self.preventRedone = preventRedone

    class Game1Details(db.Model):
        __tablename__ = "Game1Details"
        id = db.Column(db.Integer, primary_key=True)
        correctCountGame1 = db.Column(db.Integer)
        wrongCountGame1 = db.Column(db.Integer)
        timeLeftGame1 = db.Column(db.Integer)
        mark1 = db.Column(db.Integer)

        def __init__(self, id, corr, wrong, timel, mark):
            self.id = id
            self.correctCountGame1 = corr
            self.wrongCountGame1 = wrong
            self.timeLeftGame1 = timel
            self.mark1 = mark
        
    class Game1Q(db.Model):
        __tablename__ = "Game1Q"
        Id = db.Column(db.Integer, primary_key=True)
        Question = db.Column(db.TEXT)
        Option1 = db.Column(db.TEXT)
        Option2 = db.Column(db.TEXT)
        Option3 = db.Column(db.TEXT)
        Option4 = db.Column(db.TEXT)
        Answer = db.Column(db.Integer)
        Random = db.Column(db.Integer)

        def __init__(self, id, q, o1, o2, o3, o4, ans, ran):
            self.Id = id
            self.Question = q
            self.Option1 = o1
            self.Option2 = o2
            self.Option3 = o3
            self.Option4 = o4
            self.Answer = ans
            self.Random = ran

    Model.Users = Users
    Model.self_db = db
    Model.player_position = player_position
    Model.Game1Q = Game1Q
    Model.Game1Details = Game1Details