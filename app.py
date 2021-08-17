from flask import Flask, render_template, redirect, flash, abort, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.cafe_model import Cafe
from extensions import db, migrate, login_manager
from models.user_model import User
from forms.cafe_form import CafeForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
import bcrypt

db_passwd = "g^))-tVb,4~JqWLL"
db_login = "postgres"
app = Flask(__name__)
app.secret_key = "082c7cb9318230a71204861ac2c6e938"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_login}:{db_passwd}@localhost/cafes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)
migrate.init_app(app=app, db=db)
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route('/cafes')
def cafes():
    return render_template("cafes.html", cafes=Cafe.query.all())


@app.route('/add', methods=["POST", "GET"])
@login_required
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe()
        form.populate_obj(new_cafe)
        new_cafe.user_id = current_user.id
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add.html", cafe_form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated is False:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user_to_login = User.query.filter_by(email=login_form.email.data).first()
            if user_to_login:
                if bcrypt.checkpw(login_form.password.data.encode("utf-8"), user_to_login.password.encode("utf-8")):
                    login_user(user_to_login)

                    return redirect(url_for("dashboard"))
            flash("Wrong credentials")

        return render_template("login.html", form=login_form)
    else:

        return redirect(url_for("dashboard"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated is False:
        register_form = RegisterForm()
        if register_form.validate_on_submit():
            if User.query.filter_by(email=register_form.email.data).first():
                flash("This email is already present in our database. Log in instead")
            elif User.query.filter_by(name=register_form.login.data).first():
                flash("This username is already present in our database. Log in instead")
            else:
                new_user = User()
                new_user.name = register_form.login.data
                new_user.email = register_form.email.data
                new_user.password = bcrypt.hashpw(register_form.password.data.encode("utf-8"),
                                                  bcrypt.gensalt(14)).decode()
                db.session.add(new_user)
                db.session.commit()
                flash("Successfully registered. You can log in now.")

            return redirect(url_for("login"))

        return render_template("register.html", form=register_form)
    else:

        return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/edit/<cafe_id>", methods=["GET", "POST"])
@login_required
def edit(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        if current_user.id == cafe.user.id:
            edit_form = CafeForm(obj=cafe)
            if edit_form.validate_on_submit():
                edit_form.populate_obj(cafe)
                db.session.commit()
                return redirect(url_for("cafes"))
            return render_template("edit.html", cafe_form=edit_form, cafe=cafe)
        else:
            abort(401)
    else:
        abort(404)


@app.route("/delete/<cafe_id>")
@login_required
def delete(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        if current_user.id == cafe.user.id:
            db.session.delete(cafe)
            db.session.commit()
            return redirect(url_for("cafes"))
        else:
            abort(401)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
