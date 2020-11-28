DEFAULT_USER = "gamehive"
DEFAULT_PASSWORD = "gamehive"

DB_URL = "postgresql://gamehive:gamehive@postgres:5432/gamehive1"
PORT_NUMBER = 5000
HOST = "0.0.0.0"
DEBUG = True
SHORT_ID_LENGTH = 7

SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_COMMIT_ON_TEARDOWN = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "AFDFdsfadsfadsf asdf dsafd"

Swagger_Template = {
    "swagger": "2.0",
    "info": {
        "title": "Short URL API Server",
        "description": "RESTful API Server for Gamehive Interview",
        "contact": {
            "responsibleDeveloper": "Yunlong Ma",
            "email": "yunlongma@gmail.com",
            "url": "https://www.linkedin.com/in/yunlong-ma-198ba9126/",
        },
        "version": "0.1",
    },
    "securityDefinitions": {"BasicAuth": {"type": "basic",}},
}


def GetConfig():
    APP_CONFIG = {}

    APP_CONFIG["Swagger_Template"] = Swagger_Template
    APP_CONFIG["DB_URL"] = DB_URL
    APP_CONFIG["PORT_NUMBER"] = PORT_NUMBER
    APP_CONFIG["HOST"] = HOST
    APP_CONFIG["DEBUG"] = DEBUG
    APP_CONFIG["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    APP_CONFIG["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = SQLALCHEMY_COMMIT_ON_TEARDOWN
    APP_CONFIG["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    APP_CONFIG["SECRET_KEY"] = SECRET_KEY
    APP_CONFIG["SHORT_ID_LENGTH"] = SHORT_ID_LENGTH
    APP_CONFIG["DEFAULT_USER"] = DEFAULT_USER
    APP_CONFIG["DEFAULT_PASSWORD"] = DEFAULT_PASSWORD

    return APP_CONFIG
