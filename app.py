from flask import Flask, render_template, redirect
from flask_wtf.form import FlaskForm
from wtforms.validators import URL, DataRequired
from wtforms import StringField, SubmitField, SelectField, DateTimeField, TimeField
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "082c7cb9318230a71204861ac2c6e938"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)
FLASK_DEBUG = 1


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    coffee_quality = db.Column(db.String(250), nullable=False)
    wifi_speed = db.Column(db.String(250), nullable=False)
    power_socket = db.Column(db.String(250), nullable=False)


class CafeForm(FlaskForm):
    cafe_name = StringField(label="Cafe name", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired(), URL()])
    open_time = TimeField(label="Opening time", format="%H:%M")
    close_time = TimeField(label="Closing time", format="%H:%M")
    coffee = SelectField(label="Coffee quality", validators=[DataRequired()],
                         choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi = SelectField(label="Wifi speed", validators=[DataRequired()],
                       choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField(label="Power socket availability", validators=[DataRequired()],
                        choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField(label="Submit")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    cafes = Cafe.query.all()
    return render_template("cafes.html", cafes=cafes)


@app.route('/add', methods=["POST", "GET"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe()
        new_cafe.name = form.cafe_name.data
        new_cafe.location = form.location.data
        new_cafe.open_time = form.open_time.data
        new_cafe.close_time = form.close_time.data
        new_cafe.coffee_quality = form.coffee.data
        new_cafe.wifi_speed = form.wifi.data
        new_cafe.power_socket = form.power.data
        db.session.add(new_cafe)
        db.session.commit()
        return redirect("cafes")
    return render_template("add.html", cafe_form=form)


if __name__ == '__main__':
    app.run()
