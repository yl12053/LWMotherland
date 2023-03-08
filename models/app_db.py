from flask_sqlalchemy import sqlalchemy
from flask_login import UserMixin, login_required, current_user
from flask import request


class Model:
  pass


def init(db, app):
  classes(db, app)
  db.init_app(app)
  with app.app_context():
    db.create_all()

  @app.route("/changeLoc", methods=["POST"])
  @login_required
  def cloc():
    q = Model.player_position.query.filter_by(id=current_user.id).first()
    if q is None:
      q = Model.player_position(current_user.id, int(request.form.get("dim")),
                                int(request.form.get("x")),
                                int(request.form.get("y")),
                                request.form.get("reserved"), 0)
      db.session.add(q)
    else:
      q.dim = int(request.form.get("dim"))
      q.x = int(request.form.get("x"))
      q.y = int(request.form.get("y"))
      q.reserved = request.form.get("reserved")
    db.session.commit()
    return "Success"


def classes(db, app):
  Model.curr_app = app
  Model.self_db = db

  class WrapperClass:

    class Users(db.Model, UserMixin):
      __tablename__ = "Auth"
      id = db.Column(db.Integer, primary_key=True)
      clas = db.Column(db.VARCHAR(255))
      cno = db.Column(db.Integer)
      grp = db.Column(db.VARCHAR(255))
      used_name = db.Column(db.VARCHAR(255))
      role = db.Column(sqlalchemy.JSON)
      subindex = db.Column(db.Integer, nullable=False)

      def __init__(self, id, clas, cno, grp, name, role=[], subindex=0):
        self.id = id
        self.clas = clas
        self.cno = cno
        self.grp = grp
        self.used_name = name
        self.role = role
        self.subindex = subindex

    class player_position(db.Model):
      __tablename__ = "player_position"
      id = db.Column(db.Integer, primary_key=True)
      dim = db.Column(db.Integer)
      x = db.Column(db.Integer)
      y = db.Column(db.Integer)
      reserved = db.Column(db.Integer)
      preventRedone = db.Column(db.Integer)
      timeStart = db.Column(db.Float)
      timeEnd = db.Column(db.Float)

      def __init__(self, id, dim, x, y, reserved, preventRedone=0, start=0, end=0):
        if preventRedone < 0:
          preventRedone = 0
        self.id = id
        self.dim = dim
        self.x = x
        self.y = y
        self.reserved = reserved
        self.preventRedone = preventRedone
        self.timeStart = start
        self.timeEnd = end

    class Game1Details(db.Model):
      __tablename__ = "Game1Details"
      id = db.Column(db.Integer, primary_key=True)
      correctCountGame1 = db.Column(db.Integer)
      wrongCountGame1 = db.Column(db.Integer)
      timeLeftGame1 = db.Column(db.Integer)
      timeBonus = db.Column(db.Integer)
      selectedQ = db.Column(sqlalchemy.JSON)

      def __init__(self, id, corr, wrong, timel, tb, sq):
        self.id = id
        self.correctCountGame1 = corr
        self.wrongCountGame1 = wrong
        self.timeLeftGame1 = timel
        self.timeBonus = tb
        self.selectedQ = sq

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

    class Game2Q(db.Model):
      __tablename__ = "Game2Q"
      id = db.Column(db.Integer, primary_key=True)
      Question = db.Column(db.TEXT)
      Options = db.Column(sqlalchemy.JSON)
      Correct = db.Column(sqlalchemy.JSON)
      Random = db.Column(db.Integer)

      def __init__(self, id, Question, Options, Correct, Random=0):
        self.id = id
        self.Question = Question
        self.Options = Options
        self.Correct = Correct
        self.Random = Random

    class Game2Details(db.Model):
      __tablename__ = "Game2Details"
      id = db.Column(db.Integer, primary_key=True)
      details = db.Column(sqlalchemy.JSON)
      marks = db.Column(db.Integer)

      def __init__(self, id, details, marks):
        self.id = id
        self.details = details
        self.marks = marks

    class Game1Bypass(db.Model):
      __tablename__ = "Game1Bypass"
      id = db.Column(db.Integer, primary_key=True)
      tipsGiven = db.Column(sqlalchemy.JSON)
      passed = db.Column(db.Integer)

      def __init__(self, id, tipsGiven, passed):
        self.id = id
        self.tipsGiven = tipsGiven
        self.passed = passed

    class Game1BQ(db.Model):
      __tablename__ = "Game1BQ"
      _id = db.Column(db.Integer, primary_key=True)
      All = db.Column(sqlalchemy.JSON)
      WrongIndex = db.Column(sqlalchemy.JSON)

      def __init__(self, _id, All, WrongIndex):
        self._id = _id
        self.All = All
        self.WrongIndex = WrongIndex

    class additional_mark(db.Model):
      __tablename__ = "additional_mark"
      id = db.Column(db.Integer, primary_key=True)
      group = db.Column(db.VARCHAR(255))
      mark = db.Column(db.Integer)

      def __init__(self, id, group, mark):
        self.id = id
        self.group = group
        self.mark = mark

  for items in WrapperClass.__dict__.keys():
    if isinstance(getattr(WrapperClass, items), type) and (db.Model in getattr(
        WrapperClass, items).__mro__):
      setattr(Model, items, getattr(WrapperClass, items))
      print("[Database] Model registered: %s" % items)
  Model.dataCompleted = set()
  Model.handle = []
  Model.nameMap = {}
  Model._initialized = True
  print("[Database] Model initialized")
