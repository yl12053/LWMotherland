from flask_sqlalchemy import SQLAlchemy


class Model:
    pass


def init(db, app):
    class_define(db)
    db.init_app(app)


def class_define(db):

    class Players(db.Model):
        __tablename__ = "Players"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.VARCHAR(255))
        uuid = db.Column(db.VARCHAR(36), unique=True)
        dim = db.Column(db.Integer)
        posx = db.Column(db.Integer)
        posy = db.Column(db.Integer)
        mark = db.Column(db.Integer)

        def __init__(self, id, name, uuid, dim, posx, posy):
            self.id = id
            self.name = name
            self.uuid = uuid
            self.dim = dim
            self.posx = posx
            self.posy = posy
            self.mark = mark
