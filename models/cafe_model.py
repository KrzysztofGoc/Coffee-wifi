from extensions import db
from helpers import get_default_cafe_thumbnail
from sqlalchemy.sql import func


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    coffee_quality = db.Column(db.Integer, nullable=False)
    wifi_speed = db.Column(db.Integer, nullable=False)
    power_socket = db.Column(db.Integer, nullable=False)
    thumbnail = db.Column(db.LargeBinary, nullable=False, default=get_default_cafe_thumbnail())
    time_created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    time_updated = db.Column(db.DateTime, nullable=False, onupdate=func.now(), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {column.name: str(getattr(self, column.name)) for column in self.__table__.columns if
                column.name not in ["user_id", "thumbnail"]}
