from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
from project.models import User, Media

@app.route("/")
def hello_world():
    users = User.query.all()
    usersArr = []
    for user in users:
        usersArr.append(user.toDict()) 
    return jsonify(usersArr)

@app.route("/media/<path:id>")
def mediafiles(id):
    media = Media.query.get(id)
    return send_from_directory(media.path, media.filename)

@app.route("/list")
def list_files():
    media = Media.query.all()
    mediaArr = []
    for media in media:
        mediaArr.append(media.toDict()) 
    return jsonify(mediaArr)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        path = app.config["MEDIA_FOLDER"]
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        db.session.add(Media(path=path, filename=filename))
        db.session.commit()
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """