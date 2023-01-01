import json
from flask import Flask, request, jsonify
from dataclasses import dataclass
from sqlalchemy import desc
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

MAX_LOOKBACK = 10

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{USERNAME}:{PASSWORD}@localhost/heartbeat"

db = SQLAlchemy(app)

# define tables schemas that needed for coming up the write to heartbeat driver endpoint
class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    heartbeat = db.relationship("Heartbeat", backref="drivers", lazy=True)


# use dataclass decorator to specify how each field should be returned from queries
@dataclass
class Heartbeat(db.Model):
    heartbeat_id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("drivers.id"))
    user_role: str = db.Column(db.String(100))
    time_stamp: int = db.Column(db.Integer)
    latitude: float = db.Column(db.Float)
    longitude: float = db.Column(db.Float)
    speed: float = db.Column(db.Float)


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
    ):
        return "Unable to write to server due to missing attribute(s)", 400

    post_heartbeat(user_id, user_role, time_stamp, latitude, longitude, speed)

    return "Heartbeat data added successfully", 200


# GET heartbeats by user_id
@app.route("/heartbeat/<int:user_id>", methods=["GET"])
@cross_origin()
def get_heartbeats_by_user_id(user_id):
    user_exists = Heartbeat.query.filter_by(user_id=user_id).first()
    lookback = request.args.get("lookback")

    # check if user_id exists
    if not user_exists:
        return f"No heartbeats found for user_id: {user_id}.", 400

    # check if lookback parameter is valid type and within range
    if lookback:
        try:
            lookback = int(lookback)
        except ValueError:
            return "Invalid type, lookback must be an integer", 400

        if lookback > MAX_LOOKBACK:
            return f"Maximum lookback limit exceeded (max: {MAX_LOOKBACK})", 400

        # get multiple heartbeats
        data = get_latest_heartbeats(user_id, lookback)

    else:
        # get single heartbeat
        data = get_latest_heartbeats(user_id)

    return jsonify(data)


if __name__ == "__main__":

    app.run(debug=True)

# helpers
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


# params
# user_id: int
# lookback: int, 1 by default
def get_latest_heartbeats(user_id, lookback=1):
    return (
        Heartbeat.query.filter_by(user_id=user_id)
        .order_by(Heartbeat.time_stamp.desc())
        .limit(lookback)
        .all()
    )
