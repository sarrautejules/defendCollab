from email import message
from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    send_from_directory,
    request,
    render_template,
    redirect,
    url_for
)
import json
from sqlalchemy import null
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
from project.models import User, Media, Dataset
from project.auth import token_required
@app.route("/")
def list_projects():
    projects = Dataset.query.all()
    return render_template('datasets.html', projects=projects)
    # usersArr = []
    # for user in users:
    #     usersArr.append(user.toDict()) 
    # return jsonify(usersArr)
@app.route("/user", methods=["GET"])
@token_required
def user(current_user):
    return jsonify({
        "message": "User profile",
        "data": {
            "email": current_user.email,
            "uuid": current_user.uuid,
            "active": current_user.active
        }
    })

@app.route("/user/login", methods=["GET","POST"])
def user_login():
    try:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).one().is_ok_login(password)
            if user != {}:
                flash(message="Logged in welcome {0}".format(user.email), category="info")
                res = make_response(render_template('login.html'))
                res.set_cookie('jwt', user.hash)
                return res
        flash(message="Invalid credentials", category="warning")
        res = make_response(render_template('login.html'))
        res.set_cookie('jwt', '', expires=0)
        return res
    except Exception as e:
        flash(message=e, category="warning")
        res = make_response(render_template('login.html'))
        res.set_cookie('jwt', '', expires=0)
        return res

@app.route("/user/register", methods=["POST"])
def user_register():
    try:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            db.session.add(User(email=email, password=password))
            db.session.commit()
            return "User created", 201
    except Exception as e:
        return "Debug error: {0}".format(e), 500

@app.route("/media/<path:id>")
def media_files(id):
    try:
        media = Media.query.get(id)
        return send_from_directory(media.path, media.filename)
    except Exception as e:
        return "Le média n'existe pas", 404

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
    try:
        dataset = Dataset.query.get(id)
        data = json.loads(dataset.config)
        return jsonify(data)
    except Exception as e:
        return "Le json a été mal formaté pour ce Dataset", 500

@app.route("/config", methods=["GET", "POST"])
@token_required
def config_path(current_user):
    try:
        if request.method == "POST":
            project = request.form.get('projectname')
            config = request.form.get('config')
            # filename = secure_filename(file.filename)
            # path = app.config["MEDIA_FOLDER"]
            # file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
            db.session.add(Dataset(projectName=project, config=config))
            db.session.commit()
        return render_template('config.html')
    except Exception as e:
        return "Une erreur est survenue {0}".format(e), 500

@app.route("/upload/<path:id>", methods=["GET", "POST"])
def upload_file(id):
    try:
        if request.method == "POST":
            file = request.files["file"]
            mimetype = file.content_type
            length = file.content_length
            filename = secure_filename(file.filename)
            path = app.config["MEDIA_FOLDER"]
            option = request.form.get('option')
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
            db.session.add(Media(path=path, filename=filename, project=id, option=option, mimetype=mimetype, length=str(length)))
            db.session.commit()
        dataset = Dataset.query.get(id)
        data = json.loads(dataset.config)
        return render_template('upload.html', title=dataset.projectName, project=data, id=dataset.id)
    except Exception as e:
        return "Le projet n'existe pas", 404