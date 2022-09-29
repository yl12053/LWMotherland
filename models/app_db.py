from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class Model:
    pass


def init(db, app):
    classes(db)
    db.init_app(app)
    with app.app_context():
        db.create_all()


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

    Model.Users = Users
    Model.self_db = db