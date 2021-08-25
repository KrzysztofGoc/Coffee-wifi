from flask import Flask, render_template, redirect, flash, abort, url_for, jsonify, request, g
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, migrate, login_manager
from models.cafe_model import Cafe
from models.user_model import User
from models.api_key_model import ApiKey
from forms.cafe_form import CafeForm
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
import bcrypt
from sqlalchemy.sql.expression import func
from secrets import token_urlsafe
from flask_expects_json import expects_json
from schemas.new_cafe_schema import new_cafe_schema
from schemas.get_cafe_schema import get_cafe_schema
from schemas.delete_cafe_schema import delete_cafe_schema
import jsonschema
import base64
from helpers import split_list, allowed_file, get_last_updated_string

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
    return render_template("dashboard.html", api_key=ApiKey.query.filter_by(user=current_user).first().key)


@app.route('/cafes')
def cafes():
    cafes = Cafe.query.all()
    for cafe in cafes:
        cafe.thumbnail = base64.b64encode(cafe.thumbnail)
        setattr(cafe, "last_updated", get_last_updated_string(cafe.time_updated))
    cafes = split_list(cafes, 3)
    return render_template("cafes.html", cafes=cafes)


@app.route('/add', methods=["POST", "GET"])
@login_required
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe()
        form.populate_obj(new_cafe)
        new_cafe.user = current_user
        if not isinstance(form.thumbnail.data, bytes):
            new_cafe.thumbnail = form.thumbnail.data.read()
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
                                                  bcrypt.gensalt()).decode()
                new_api_key = ApiKey(key=token_urlsafe(32), user=new_user)
                db.session.add(new_user, new_api_key)
                db.session.commit()
                flash("Successfully registered. You can log in now.")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", form=register_form)
    else:
        return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out.")
    return redirect(url_for("login"))


@app.route("/edit/<cafe_id>", methods=["GET", "POST"])
@login_required
def edit(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        if current_user == cafe.user:
            edit_form = CafeForm(obj=cafe)
            if edit_form.validate_on_submit():
                edit_form.populate_obj(cafe)
                if not isinstance(edit_form.thumbnail.data, bytes):
                    cafe.thumbnail = edit_form.thumbnail.data.read()
                db.session.commit()
                return redirect(url_for("cafes"))
            return render_template("edit.html", cafe_form=edit_form, cafe=cafe)
    abort(404)


@app.route("/delete/<cafe_id>")
@login_required
def delete(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        if current_user == cafe.user:
            db.session.delete(cafe)
            db.session.commit()
            return redirect(url_for("cafes"))
    abort(404)


@app.route("/a/cafes/random", methods=["GET"])
def random_cafe():
    rand_cafe = Cafe.query.order_by(func.random()).first()
    return jsonify(cafe=rand_cafe.to_dict())


@app.route("/a/cafes", methods=["GET", "POST"])
def all_cafes():
    if request.method == "GET":
        try:
            jsonschema.validate(instance=dict(request.args), schema=get_cafe_schema)
        except jsonschema.ValidationError as e:
            return jsonify(message=e.message), 400
        else:
            found_cafes = Cafe.query.filter_by(**request.args).all()
            if found_cafes:
                return jsonify(cafes=[cafe.to_dict() for cafe in found_cafes])
            else:
                return jsonify(message="Resource not found"), 404

    elif request.method == "POST":
        new_cafe_data = {}
        thumbnail = request.files.get("thumbnail")
        if thumbnail:
            if thumbnail.filename == "":
                return jsonify(message="Wrong thumbnail filename."), 400
            if not allowed_file(thumbnail.filename):
                return jsonify(message="Wrong thumbnail file extension."), 400
            new_cafe_data["thumbnail"] = thumbnail.read()
        try:
            jsonschema.validate(instance=dict(request.form), schema=new_cafe_schema)
        except jsonschema.ValidationError as e:
            return jsonify(message=f"{e.path.pop()} - {e.message} - {e.schema}"), 400
        else:
            new_cafe_data.update(dict(request.form))
            api_key = ApiKey.query.filter_by(key=new_cafe_data.pop("token")).first()
            if api_key:
                db.session.add(Cafe(**new_cafe_data, user=api_key.user))
                db.session.commit()
                return jsonify(message="Successfully added new cafe to database."), 201
            else:
                return jsonify(message="Wrong token provided."), 401


@app.route("/a/cafes/<int:cafe_id>", methods=["GET", "PUT", "DELETE"])
@expects_json(schema=delete_cafe_schema, ignore_for=["GET", "PUT"])
def get_cafe(cafe_id):
    if request.method == "GET":
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            return jsonify(cafe=cafe.to_dict()), 200
        else:
            return jsonify(message="Resource not found"), 404
    elif request.method == "PUT":
        edit_cafe_data = {}
        thumbnail = request.files.get("thumbnail")
        if thumbnail:
            if thumbnail.filename == "":
                return jsonify(message="Wrong thumbnail filename."), 400
            if not allowed_file(thumbnail.filename):
                return jsonify(message="Wrong thumbnail file extension."), 400
            edit_cafe_data["thumbnail"] = thumbnail.read()
        try:
            jsonschema.validate(instance=dict(request.form), schema=new_cafe_schema)
        except jsonschema.ValidationError as e:
            return jsonify(message=e.message), 400
        else:
            edit_cafe_data.update(dict(request.form))
            api_key = ApiKey.query.filter_by(key=edit_cafe_data.pop("token")).first()
            selected_cafe = Cafe.query.get(cafe_id)
            if api_key:
                if selected_cafe:
                    if selected_cafe.user == api_key.user:
                        db.session.delete(selected_cafe)
                        db.session.add(Cafe(**edit_cafe_data, user=api_key.user))
                        db.session.commit()
                        return jsonify(message="Successfully updated resource."), 200
                    else:
                        return jsonify(message="No permission to delete resource."), 401
                else:
                    return jsonify(message="Resource not found"), 404
            else:
                return jsonify(message="Wrong token provided."), 401
    elif request.method == "DELETE":
        token = g.data.get("token")
        api_key = ApiKey.query.filter_by(key=token).first()
        selected_cafe = Cafe.query.get(cafe_id)
        if api_key:
            if selected_cafe:
                if selected_cafe.user == api_key.user:
                    db.session.delete(selected_cafe)
                    db.session.commit()
                    return jsonify(message="Successfully deleted resource"), 200
                else:
                    return jsonify(message="No permission to delete resource."), 401
            else:
                return jsonify(message="Resource not found"), 404
        else:
            return jsonify(message="Wrong token provided"), 401


if __name__ == '__main__':
    app.run()
