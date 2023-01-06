import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

MAX_LOOKBACK = 10

# retrive the heartbeat table from DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)
table = dynamodb.Table("heartbeat")

# returns all heartbeat data in dynamodb
@app.route("/heartbeat", methods=["GET"])
@cross_origin()
def get_all_heartbeat():
    response = table.scan()["Items"]
    return jsonify(response)

@app.route("/heartbeat", methods=["POST"])
@cross_origin()
def heartbeatpost():
    data = json.loads(request.get_data())
    user_id = data["user_id"]
    time_stamp = data["time_stamp"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    speed = data["speed"]

    if (
        not user_id
        or not time_stamp
        or not latitude
        or not longitude
    ):
        return "Unable to write"

    post_heartbeat(user_id, time_stamp, latitude, longitude, speed)
    return "Heartbeat data added successfully", 200

def post_heartbeat(id, time_stamp, lat, long, speed):

    table.put_item(
        Item={
            "userId": id,
            "timestamp": time_stamp,
            "latitude": Decimal(str(lat)),
            "longitude": Decimal(str(long)),
            "speed": speed,
        }
    )

# GET heartbeats by user_id
@app.route("/heartbeat/<user_id>", methods=["GET"])
@cross_origin()
def get_heartbeats_by_user_id(user_id):
    # convert user_id to a integer, otherwise the post request will be return a 500 error message
    user_id = str(user_id)

    # create a lookback variable to retrive the lookback value after th
    lookback = request.args.get("lookback")

    # check if lookback parameter is valid type and within range
    if lookback:
        try:
            lookback = int(lookback)
        except ValueError:
            return "Invalid type, lookback must be an integer", 400

        if lookback > MAX_LOOKBACK:
            return f"Maximum lookback limit exceeded (max: {MAX_LOOKBACK})", 400

        data = get_latest_heartbeats(user_id, lookback)

    else:
        # get single heartbeat
        data = get_latest_heartbeats(user_id)

    # return requested heartbeat data to user
    return jsonify(data["Items"])

def get_latest_heartbeats(user_id, lookback=1):
    user_id = str(user_id)
    return table.query(
        # make a query from heartbeat table, and return all the heartbeat record that match with the queried user_id
        KeyConditionExpression=Key("userId").eq(user_id),
        # sort time_stamp(Sort key) by decending order
        ScanIndexForward=False,
        # set the number of returning data limit
        Limit=lookback,
    )
