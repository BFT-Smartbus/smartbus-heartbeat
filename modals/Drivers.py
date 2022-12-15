from config import db

class Drivers(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100))
  password = db.Column(db.String(100))
  heartbeat = db.relationship('HeartbeatDriver', backref='drivers', lazy=True)