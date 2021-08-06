from flask import Flask, render_template, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models.cafe_model import db, Cafe
from models.user_model import User
from forms.cafe_form import CafeForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from flask_migrate import Migrate
import bcrypt

app = Flask(__name__)
app.secret_key = "082c7cb9318230a71204861ac2c6e938"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("login.html")


@app.route('/cafes')
def cafes():
    return render_template("cafes.html", cafes=Cafe.query.all())


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


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_to_login = User.query.filter_by(email=login_form.email.data).first()
        if user_to_login:
            if bcrypt.checkpw(login_form.password.data.encode("utf8"), user_to_login.password):
                login_user(user_to_login)
                return redirect("dashboard")
        flash("Wrong credentials")
        return redirect("login")
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(email=register_form.email.data):
            flash("This email is already present in our database. Log in instead")
            return redirect("login")
        else:
            new_user = User()
            new_user.name = register_form.login.data
            new_user.email = register_form.email.data
            new_user.password = bcrypt.hashpw(register_form.password.data.encode("utf8"), bcrypt.gensalt(14))
            db.session.add(new_user)
            db.session.commit()
            return redirect("/")
    return render_template("register.html", form=register_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("login")


if __name__ == '__main__':
    app.run()
