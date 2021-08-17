from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(100), unique=True)
    password = db.Column(db.VARCHAR(250))
    name = db.Column(db.VARCHAR(100))
    cafes = db.relationship("Cafe", backref="user")
    db.UniqueConstraint("email", "name", name="uix_1")
