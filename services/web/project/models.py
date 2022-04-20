from project import db, app
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def is_ok_login(self, password):
        if check_password_hash(self.password, password):
            hash = jwt.encode({
                "email": self.email
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
            )
            self.hash = hash
            return self
        else : 
         return {}

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    project = db.Column(db.String(255), nullable=False)
    option = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, path, filename, project, option):
        self.path = path
        self.filename = filename
        self.project = project
        self.option = option

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Dataset(db.Model):
    __tablename__ = "datasetproject"

    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(255), unique=True, nullable=False)
    config = db.Column(db.Text(), nullable=False)

    def __init__(self, projectName, config):
        self.projectName = projectName
        self.config = config

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }