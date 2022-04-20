from project import db
from sqlalchemy import inspect

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), unique=True, nullable=False)
    filename = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }