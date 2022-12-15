from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = 'SOMEPASSWORD'
SQLALCHEMY_DATABASE_URI = 'sqlite:///heartbeat.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
