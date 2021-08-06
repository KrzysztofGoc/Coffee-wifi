from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL


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