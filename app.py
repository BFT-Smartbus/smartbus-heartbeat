import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

SECRET_KEY = 'SOMEPASSWORD'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///heartbeat.sqlite'
db.init_app(app)

class Drivers(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100))
  password = db.Column(db.String(100))
  heartbeat = db.relationship('HeartbeatDriver', backref='drivers', lazy=True)

class HeartbeatDriver(db.Model):
  heartbeat_id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
  user_role = db.Column(db.String(100))
  time_stamp = db.Column(db.Integer)
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)
  speed = db.Column(db.Float)


with app.app_context():
    db.create_all()


@app.route('/heartbeatdriverpost', methods=['POST'])
def heartbeatpost():
      data = json.loads(request.get_data())

      if not data['userId'] or not data['userRole'] or not data['timeStamp'] or not data['latitude'] or not data['longitude'] or not data['speed']:
        return "unable to write to server", 400
        
      else:
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
      

if __name__ == "__main__":

  app.run(debug=True)