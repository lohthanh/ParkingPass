from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.keycard_model import Keycard
from flask_app.models.user_model import User


@app.route('/keycards/create', methods=['POST'])
def create_keycard():
    Keycard.create(request.form)
    return redirect(f"/dashboard")

@app.route('/keycards/form')
def form():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    logged_user = User.get_by_id(data)
    if not logged_user:
        return redirect("/")
    return render_template('form.html', logged_user=logged_user)