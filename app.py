import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

# os, dotenv, and load_dotenv() are what we need to use .env to hide confidential code
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USERNAME}:{PASSWORD}@localhost/heartbeat"
db = SQLAlchemy(app)

# define tables schemas that needed for coming up the write to heartbeat driver endpoint


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    heartbeat = db.relationship("Heartbeat", backref="drivers", lazy=True)


class Heartbeat(db.Model):
    heartbeat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))
    user_role = db.Column(db.String(100))
    time_stamp = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    speed = db.Column(db.Float)


with app.app_context():
    db.create_all()

# endpoint, the business logic to accept data from FE and write to HeartbeatDriver table


@app.route("/heartbeat", methods=["POST"])
@cross_origin()
def heartbeatpost():
    data = json.loads(request.get_data())
    user_id = data["userId"]
    user_role = data["userRole"]
    time_stamp = data["timestamp"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    speed = data["speed"]

    if (
        not user_id
        or not user_role
        or not time_stamp
        or not latitude
        or not longitude
        or not speed
    ):
        return "unable to write to server", 400

    post_heartbeat(user_id, user_role, time_stamp, latitude, longitude, speed)

    return "heartbeat data added successfully", 200


if __name__ == "__main__":

    app.run(debug=True)


def post_heartbeat(id, role, timestamp, lat, long, speed):

    heartbeat_record = Heartbeat(
        user_id=id,
        user_role=role,
        time_stamp=timestamp,
        latitude=lat,
        longitude=long,
        speed=speed,
    )

    db.session.add(heartbeat_record)
    db.session.commit()
