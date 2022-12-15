import config
from flask import Flask
from config import db
from handler.heartbeat_driver_post import heartbeat_post
from modals.Heartbeat_driver import HeartbeatDriver
from modals.Drivers import Drivers


app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

app.register_blueprint(heartbeat_post)

with app.app_context():
    db.create_all()


if __name__ == "__main__":

  app.run(debug=True)