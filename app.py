from flask import Flask, render_template, redirect
from flask_wtf.form import FlaskForm
from wtforms.validators import URL, DataRequired
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
app.secret_key = "082c7cb9318230a71204861ac2c6e938"
Bootstrap(app)
FLASK_DEBUG = 1


class CafeForm(FlaskForm):
    cafe_name = StringField(label="Cafe name", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired(), URL()])
    open_time = DateTimeField(label="Opening time", format="%H:%M")
    close_time = DateTimeField(label="Closing time", format="%H:%M")
    coffee = SelectField(label="Coffee quality", validators=[DataRequired()], choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
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
    cafes = []
    with open("cafe_data.csv", newline='', encoding="utf8", mode="r") as cafe_data:
        cafe_data_reader = csv.reader(cafe_data)
        for row in cafe_data_reader:
            cafes.append(row)
    return render_template("cafes.html", cafes=cafes)


@app.route('/add', methods=["POST", "GET"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe_data.csv", newline='', encoding="utf8", mode="a") as cafe_data:
            cafe_data_writer = csv.writer(cafe_data)
            new_row = [form.cafe_name.data, form.location.data, form.open_time.raw_data[0], form.close_time.raw_data[0],
                       form.coffee.data, form.wifi.data, form.power.data]
            cafe_data_writer.writerow(new_row)
        return redirect("cafes")
    return render_template("add.html", cafe_form=form)


if __name__ == '__main__':
    app.run()
