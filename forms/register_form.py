from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = StringField(label="E-mail", validators=[DataRequired(), Email()])
    login = StringField(label="Login", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=10, message="Password has to be at least 10 characters long."), DataRequired()])
    submit = SubmitField(label="")