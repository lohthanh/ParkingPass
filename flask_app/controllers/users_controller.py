from datetime import datetime
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")


@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate_data(request.form):
        return redirect("/")
    hashed_pass = bcrypt.generate_password_hash(request.form["password"])
    data = {**request.form, "password": hashed_pass, "confirm_password": hashed_pass}
    logged_user_id = User.create(data)
    session["user_id"] = logged_user_id
    return redirect("/dashboard")


@app.route("/users/login", methods=["POST"])
def login_user():
    data = {"email": request.form["email"]}
    potential_user = User.get_by_email(data)

    if not potential_user:
        flash("Invalid credentials", "login")
        print("User Not Found")
        return redirect("/")
    
    if not bcrypt.check_password_hash(
        potential_user.password, request.form["password"]
    ):
        flash("Invalid credentials", "login")
        print("Invalid Password")
        return redirect("/")
    
    session["user_id"] = potential_user.id
    User.update_last_logged_on(potential_user.id)
    print(potential_user.id)
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    logged_user = User.get_by_id(data)
    if not logged_user:
        return redirect("/")
    all_users = User.get_all_users()
    return render_template(
        "dashboard.html", logged_user=logged_user, all_users=all_users
    )

@app.route("/users/<int:id>/view")
def view_info(id):
    session_data = {"id": session["user_id"]}
    logged_user = User.get_by_id(session_data)
    if not logged_user:
        return redirect("/")
    data = {"id": id}
    one_user = User.get_one_user(data)
    last_logged_on = one_user.get_last_logged_on()
    return render_template(
        "info.html", one_user=one_user, last_logged_on=last_logged_on, logged_user=logged_user
    )

@app.route('/users/<int:id>/edit')
def edit_user(id):
    data = {
        'id' : id
    }
    one_user = User.get_one_user(data)
    return render_template('edit.html', one_user=one_user)

@app.route('/users/<int:id>/update', methods=['POST'])
def update(id):
    data = {
        **request.form,
        'id' : id
    }
    User.update(data)
    return redirect(f'/users/{id}/view')

@app.route('/users/<int:id>/update', methods=['POST'])
def update(id):
    data = {
        **request.form,
        'id' : id
    }
    User.update(data)
    return redirect(f'/users/{id}/view')

@app.route('/users/delete/<int:user_id>')
def delete(user_id):
    User.delete(user_id)
    return redirect('/dashboard')


@app.route("/users/logout")
def logout():
    del session["user_id"]
    return redirect("/")
