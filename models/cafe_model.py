from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    coffee_quality = db.Column(db.String(250), nullable=False)
    wifi_speed = db.Column(db.String(250), nullable=False)
    power_socket = db.Column(db.String(250), nullable=False)
