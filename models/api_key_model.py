from extensions import db


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
