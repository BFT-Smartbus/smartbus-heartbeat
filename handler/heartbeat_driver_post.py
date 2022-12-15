import json
from flask import request, Blueprint
from modals.Heartbeat_driver import HeartbeatDriver
from config import db

heartbeat_post = Blueprint('heartbeat_post', __name__)

@heartbeat_post.route('/heartbeatdriverpost', methods=['POST'])
def heartbeatpost():
      data = json.loads(request.get_data())
      
      heartbeat_record = HeartbeatDriver(
            user_id=data['userId'],
            user_role=data['userRole'],
            time_stamp=data['timeStamp'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            speed=data['speed'])

      db.session.add(heartbeat_record)
      db.session.commit()

      return "heartbeat data added successfully", 200
