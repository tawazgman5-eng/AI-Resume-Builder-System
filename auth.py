from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])



auth = Blueprint("auth", __name__)

# REGISTER
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists.")
            return redirect("/register")

        user = User(
            full_name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")


# LOGIN
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid login")
            return redirect("/login")

        session["user_id"] = user.id
        session["user_name"] = user.full_name

        return redirect("/dashboard")

    return render_template("login.html")

from datetime import datetime, timedelta
import uuid

from itsdangerous import URLSafeTimedSerializer
from flask import render_template, request, redirect, url_for, flash
import os

def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found", "danger")
            return redirect(url_for("auth.forgot_password"))

        # ✅ Generate token
        serializer = get_serializer()
        token = serializer.dumps(email, salt="reset-password")

        # ✅ Build URL
        reset_url = url_for("auth.reset_password", token=token, _external=True)

        # ✅ Send reset URL to page instead of console
        return render_template(
            "reset_link.html",
            reset_url=reset_url,
            email=email
        )

    return render_template("forgot_password.html")


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        serializer = get_serializer()

        # ✅ Try to decode token (valid for 30 minutes)
        email = serializer.loads(
            token,
            salt="reset-password",
            max_age=1800
        )

    except Exception as e:
        return "Invalid or expired link ❌"

    # ✅ If POST (new password submitted)
    if request.method == "POST":
        new_password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return "User no longer exists ❌"

        user.set_password(new_password)
        db.session.commit()

        return "Password reset successful ✅"

    return render_template("reset_password.html", email=email)





# LOGOUT
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
