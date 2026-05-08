import re

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from ..db import db
from ..models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _bad_request(message):
    return jsonify(error=message), 400


def _conflict(message):
    return jsonify(error=message), 409


def _unauthorized(message):
    return jsonify(error=message), 401


def _validate_credentials(payload):
    if not payload:
        return None, "Please fill all required fields"

    username = (payload.get("username") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not username or not email or not password:
        return None, "username, email, and password are required"

    if len(username) < 3:
        return None, "username must be at least 3 characters"

    if len(password) < 8:
        return None, "password must be at least 8 characters"

    if not EMAIL_RE.match(email):
        return None, "email is invalid"

    return {"username": username, "email": email, "password": password}, None

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    data, error = _validate_credentials(
        request.get_json(silent=True) or request.form.to_dict()
    )
    confirm_password = request.form.get("confirm_password", "")
    if error:
        return render_template(
            "register.html",
            error=error,
        ), 400

    if data["password"] != confirm_password:
        return render_template(
            "register.html",
            error="Passwords do not match",
        ), 400

    if User.query.filter_by(username=data["username"]).first():
        return render_template(
            "register.html",
            error="Username already exists",
        ), 409

    if User.query.filter_by(email=data["email"]).first():
        return render_template(
            "register.html",
            error="Email already exists",
        ), 409

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return render_template(
            "register.html",
            error="Unable to create account",
        ), 500

    login_user(user)
    return redirect(url_for("main.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    payload = request.get_json(silent=True) or request.form.to_dict()
    identifier = (payload.get("identifier") or "").strip().lower()
    password = payload.get("password") or ""

    if not identifier or not password:
        return render_template(
            "login.html",
            error="Identifier and password are required",
        ), 400

    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()
    if not user or not user.check_password(password):
        return render_template(
            "login.html",
            error="Invalid credentials",
        ), 401

    login_user(user)
    return redirect(url_for("main.dashboard"))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    if not current_user.is_authenticated:
        return _unauthorized("not authenticated")

    logout_user()
    from flask import redirect, url_for
    return redirect(url_for("main.home"))