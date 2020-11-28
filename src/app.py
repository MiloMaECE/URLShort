from flask import Flask
from flask import request, jsonify, redirect
import re
import string
import random
import time
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import database_exists, create_database, drop_database
from flasgger import Swagger
from app_config import GetConfig

APP_CONFIG = GetConfig()
DEFAULT_USER = APP_CONFIG["DEFAULT_USER"]
DEFAULT_PASSWORD = APP_CONFIG["DEFAULT_PASSWORD"]
DB_URL = APP_CONFIG["DB_URL"]
PORT_NUMBER = APP_CONFIG["PORT_NUMBER"]
HOST = APP_CONFIG["HOST"]
DEBUG = APP_CONFIG["DEBUG"]
SHORT_ID_LENGTH = APP_CONFIG["SHORT_ID_LENGTH"]

SQLALCHEMY_DATABASE_URI = APP_CONFIG["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_COMMIT_ON_TEARDOWN = APP_CONFIG["SQLALCHEMY_COMMIT_ON_TEARDOWN"]
SQLALCHEMY_TRACK_MODIFICATIONS = APP_CONFIG["SQLALCHEMY_TRACK_MODIFICATIONS"]
SECRET_KEY = APP_CONFIG["SECRET_KEY"]

Swagger_Template = APP_CONFIG["Swagger_Template"]


class ServerConfig(object):
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_COMMIT_ON_TEARDOWN = SQLALCHEMY_COMMIT_ON_TEARDOWN
    SQLALCHEMY_TRACK_MODIFICATIONS = SQLALCHEMY_TRACK_MODIFICATIONS
    SECRET_KEY = SECRET_KEY


app = Flask(__name__)
app.config.from_object(ServerConfig)
db = SQLAlchemy(app)
swagger = Swagger(app, template=Swagger_Template)
auth = HTTPBasicAuth()

## DataBase Model Design
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    password_hash = db.Column(db.String)
    urls = db.relationship("Url", backref="user")

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {"id": self.id, "exp": time.time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return
        return User.query.get(data["id"])


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    shorten_url_code = db.Column(db.String, index=True)
    origin_url = db.Column(db.String)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"))


try:
    User.query.filter_by(username=DEFAULT_USER).first()
except:
    if not database_exists(DB_URL):
        print("Creating database.")
        create_database(DB_URL)
        time.sleep(1)

    print("Creating tables.")
    db.create_all()
    time.sleep(1)

userquery = User.query.filter_by(username=DEFAULT_USER).first()
if userquery is None:
    user = User(username="gamehive")
    user.hash_password("gamehive")
    db.session.add(user)
    db.session.commit()

## Helper Functions


@auth.verify_password
def verify_password(user_token, password):
    user = User.verify_auth_token(user_token)
    if not user:
        user = User.query.filter_by(username=user_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.cli.command("resetdb")
def resetdb_command():
    if database_exists(DB_URL):
        print("Deleting database.")
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print("Creating database.")
        create_database(DB_URL)

    print("Creating tables.")
    db.create_all()

    user = User(username="gamehive")
    user.hash_password("gamehive")
    db.session.add(user)
    db.session.commit()


def query2json(model_list):
    lst = []

    if model_list:
        if isinstance(model_list, list):
            if isinstance(model_list[0], db.Model):
                for model in model_list:
                    dic = {}
                    for col in model.__table__.columns:
                        dic[col.name] = getattr(model, col.name)
                    lst.append(dic)
            else:
                for result in model_list:
                    lst.append([dict(zip(result.keys, r)) for r in result])
        elif isinstance(model_list, db.Model):
            dic = {}
            for col in model_list.__table__.columns:
                dic[col.name] = getattr(model_list, col.name)
            lst.append(dic)
        elif isinstance(model_list, dict):
            lst.append(dict(zip(model_list.keys(), model_list)))

    return lst


def validate_url(url):
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(regex.match(url))


def gen_short_id(length=SHORT_ID_LENGTH):
    return "".join(random.sample(string.digits + string.ascii_letters, length))


## Routing


@app.route("/signup", methods=["POST"])
def new_user():
    """Endpoint for creating a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
              username:
                type: string
                example: 'newuser'
              password:
                type: string
                example: 'password'
    responses:
      201:
        description: Successfully create a new user
        schema:
            type: object
            properties:
              status:
                type: string
                example: 'success'
              username:
                type: string
                example: 'newuser'
              userid:
                type: int
                example: 1
      200:
        description: Fail to create a new user
        schema:
            type: object
            properties:
              status:
                type: string
                example: 'fail'
              error:
                type: string
                example: 'No Username or No Password'

    """
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        res = {"status": "fail", "error": "No Username or No Password"}
        code = 200
    elif User.query.filter_by(username=username).first() is not None:
        res = {
            "status": "fail",
            "error": "Duplicate Usernames. Please choose a new one.",
        }
        code = 200
    else:
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        res = {
            "status": "success",
            "username": user.username,
            "userid": user.id,
        }
        code = 201

    return (jsonify(res), code)


@app.route("/token")
@auth.login_required
def get_auth_token():
    """Return auth token for the current user(require login using HTTP BasicAuth)
    ---
    security:
        - BasicAuth: []

    responses:
      401:
        description: Unauthorized Access
      200:
        description: Show Token for Current User
        schema:
            type: object
            properties:
              token:
                type: string
                example: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjA2NTIwNzcwLjA2ODU2OH0.CK2RBbyo17dJeALC7k6u-yQsUHz4n8ETFcBKfwE4tco'
              duration:
                type: integer
                example: 600

    """
    token = g.user.generate_auth_token(600)
    return jsonify({"token": token.decode("ascii"), "duration": 600})


@app.route("/")
def root():
    return "Welcome Shorten URL API"


@app.route("/allurls")
@auth.login_required
def get_urls():
    """Return all  Shorten URLs created by the current user
    ---
    security:
        - BasicAuth: []

    responses:
      200:
        description: Successfully feteched URLs
        schema:
            type: object
            properties:
              status:
                type: string
                example: 'success'
              username:
                type: string
                example: 'TestUser'
              userid:
                type: int
                example: 1
              url_pairs:
                type: array
                items:
                  type: object
                  properties:
                    origin_url:
                        type: string
                        example: 'https://www.youtube.com/watch?v=Rj_r07nf2d0'
                    shorten_url:
                        type: string
                        example: 'http://localhost:5000/1Y9dAPj'
                    shorten_url_code:
                        type: string
                        example: '1Y9dAPj'
      401:
        description: Unauthorized Access

    """
    user = g.user
    query_res = Url.query.filter_by(userid=user.id).all()
    query_res = query2json(query_res)

    for data in query_res:
        data.pop("id", None)
        data.pop("userid", None)
        data["shorten_url_code"] = data["shorten_url_code"]
        data["shorten_url"] = request.url_root + data["shorten_url_code"]

    res = {
        "status": "success",
        "username": user.username,
        "userid": user.id,
        "url_pairs": query_res,
    }

    return jsonify(res)


@app.route("/submit", methods=["POST"])
@auth.login_required(optional=True)
def url_shorten():
    """Return all  Shorten URLs created by the current user
    ---

    parameters:
      - name: body
        in: body
        required: true
        schema:
            type: object
            properties:
              url:
                type: string
                example: 'https://www.youtube.com/watch?v=Rj_r07nf2d0'

    security:
        - BasicAuth: []

    responses:
      200:
        description: Stored the URL pair in PostGresSQL database and Return Shorten URL Code
        schema:
            type: object
            properties:
              status:
                type: string
                example: 'success'
              username:
                type: string
                example: 'newuser'
              userid:
                type: int
                example: 2
              origin_url:
                type: string
                example: 'https://www.youtube.com/watch?v=Rj_r07nf2d0'
              shorten_url_code:
                type: string
                example: '1Y9dAPj'
              shorten_url:
                type: string
                example: 'http://localhost:5000/1Y9dAPj'
    """
    try:
        user = g.user
    except:
        user = {}

    post_content = request.json
    origin_url = post_content.get("url")

    if validate_url(origin_url):
        shorten_url_code = gen_short_id()

        while Url.query.filter_by(shorten_url_code=shorten_url_code).first() is not None:
            shorten_url_code = gen_short_id()

        shorten_url = request.url_root + shorten_url_code

        if user:
            new_url_pair = Url(
                origin_url=origin_url, shorten_url_code=shorten_url_code, userid=user.id
            )
            res = {
                "status": "success",
                "origin_url": origin_url,
                "shorten_url_code": shorten_url_code,
                "shorten_url": shorten_url,
                "userid": user.id,
                "username": user.username,
            }
        else:
            new_url_pair = Url(origin_url=origin_url, shorten_url_code=shorten_url_code)
            res = {
                "status": "success",
                "origin_url": origin_url,
                "shorten_url_code": shorten_url_code,
                "shorten_url": shorten_url,
                "userid": None,
                "username": None,
            }

        db.session.add(new_url_pair)
        db.session.commit()

    else:
        res = {"status": "fail", "error": "Request Url Is Not A Valid Url"}

    return jsonify(res)


@app.route("/<shorten_url_code>")
def expand_url(shorten_url_code):
    """Return all  Shorten URLs created by the current user
    ---

    parameters:
      - name: shorten_url_code
        in: path
        required: true
        schema:
            type: string
        example: 1Y9dAPj

    responses:
      302:
        description: Successfully find the original URL and redirect to it. Swagger may display a TypeError because it will always follow the redirect links. The logic is normal and could be tested by curl, postman and browser.
      200:
        description: Fail to find the shorten url in the database
        schema:
            type: object
            properties:
              status:
                type: string
                example: 'fail'
              error:
                type: string
                example: 'Shorten Url Not Found'


    """
    query_res = Url.query.filter_by(shorten_url_code=shorten_url_code).first()

    if query_res:
        query_res = query2json(query_res)

        return redirect(query_res[0].get("origin_url"), code=302)
    else:
        res = {"status": "fail", "error": "Shorten Url Not Found"}
        return jsonify(res)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT_NUMBER, debug=DEBUG)
