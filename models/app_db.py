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

        def __init__(self, id, clas, cno, grp):
            self.id = id
            self.clas = clas
            self.cno = cno
            self.grp = grp

    Model.Users = Users