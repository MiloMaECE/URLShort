from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://gamehive:gamehive@postgres:5432/gamehive"


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route("/")
def root():
    return "Game Hive Player API"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
