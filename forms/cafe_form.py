from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired
from helpers import get_default_cafe_thumbnail


class CafeForm(FlaskForm):
    name = StringField(label="Cafe name", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    open_time = TimeField(label="Opening time", format="%H:%M")
    close_time = TimeField(label="Closing time", format="%H:%M")
    coffee_quality = SelectField(label="Coffee quality", validators=[DataRequired()],
                                 choices=[(1, "☕"), (2, "☕☕"), (3, "☕☕☕"), (4, "☕☕☕☕"), (5, "☕☕☕☕☕")])
    wifi_speed = SelectField(label="Wifi speed", validators=[DataRequired()],
                             choices=[(0, "✘"), (1, "💪"), (2, "💪💪"), (3, "💪💪💪"), (4, "💪💪💪💪"), (5, "💪💪💪💪💪")])
    power_socket = SelectField(label="Power socket availability", validators=[DataRequired()],
                               choices=[(1, "🔌"), (2, "🔌🔌"), (3, "🔌🔌🔌"), (4, "🔌🔌🔌🔌"), (5, "🔌🔌🔌🔌🔌")])
    thumbnail = FileField(label="Cafe thumbnail", default=get_default_cafe_thumbnail())
    submit = SubmitField(label="Submit")
