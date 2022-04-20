from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    render_template,
    redirect,
    url_for
)
import json
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
from project.models import User, Media, Dataset

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

@app.route("/configlist")
def list_config():
    dataset = Dataset.query.all()
    datasetArr = []
    for dataset in dataset:
        datasetArr.append(dataset.toDict()) 
    return jsonify(datasetArr)

@app.route("/configlist/option/<path:id>")
def get_config(id):
    dataset = Dataset.query.get(id)
    data = json.loads(dataset.config)
    return jsonify(data)

@app.route("/config", methods=["GET", "POST"])
def config_path():
    if request.method == "POST":
        project = request.form.get('projectname')
        config = request.form.get('config')
        # filename = secure_filename(file.filename)
        # path = app.config["MEDIA_FOLDER"]
        # file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        db.session.add(Dataset(projectName=project, config=config))
        db.session.commit()
    return render_template('config.html')

@app.route("/upload/<path:id>", methods=["GET", "POST"])
def upload_file(id):
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        path = app.config["MEDIA_FOLDER"]
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        db.session.add(Media(path=path, filename=filename))
        db.session.commit()
    dataset = Dataset.query.get(id)
    data = json.loads(dataset.config)
    return render_template('upload.html', title=dataset.projectName, project=data)