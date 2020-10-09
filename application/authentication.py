from flask import Blueprint, session, render_template, redirect, url_for, request
from application.models import *
from werkzeug.security import check_password_hash, generate_password_hash
from application.auth_util import *
import random
from functools import wraps

bp = Blueprint("authentication", __name__, url_prefix='/authentication')

@bp.route("/", methods=["POST", "GET"])
def login():
    if session.get("administrator"):
        return redirect(url_for('administrator.homepage'))
    elif session.get("siteuser"):
        return redirect(url_for('siteuser.homepage'))
    
    if session.get("registration"):
        session["registration"].clear()
        session["registration"] = None

    if request.method == "GET":
        return render_template(
            "authentication/login.html"
        )
    
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return render_template(
            "authentication/login.html",
            login_error="Enter your email address and password."
        )
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return render_template(
            "authentication/login.html",
            login_error="Incorrect email address or password."
        )

    if user.admin:
        session["administrator"] = {
            "name": user.name,
            "mobile": user.mobile,
            "email": user.email,
            "username": user.username,
            "id": user.id
        }
        return redirect(url_for('administrator.homepage'))
    else:
        session["siteuser"] = {
            "name": user.name,
            "mobile": user.mobile,
            "email": user.email,
            "username": user.username,
            "id": user.id
        }
        return redirect(url_for('siteuser.homepage'))


@bp.route("/register", methods=["POST", "GET"])
def register():
    if session.get("administrator"):
        return redirect(url_for('administrator.homepage'))
    elif session.get("siteuser"):
        return redirect(url_for('siteuser.homepage'))
    
    if request.method == "GET":
        if session.get("registration"):
            session["registration"].clear()
            session["registration"] = None
        return render_template(
            "authentication/register.html"
        )
    
    name = request.form.get("name")
    mobile = request.form.get("mobile")
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    if not name or not mobile or not email or not username or not password1 or not password2:
        return render_template(
            "authentication/register.html",
            register_error="All fields marked with (*) are required"
        )
    
    name = name.strip().title()
    mobile = mobile.strip()
    email = email.strip()
    username = username.strip()

    if password2 != password1:
        return render_template(
            "authentication/register.html",
            register_error="Passwords don't match."
        )
    
    if not validate_email(email):
        return render_template(
            "authentication/register.html",
            register_error="Invalid email address."
        )
    
    if not validate_mobile(mobile):
        return render_template(
            "authentication/register.html",
            register_error="Invalid mobile number."
        )
    
    if not validate_password(password1):
        return render_template(
            "authentication/register.html",
            register_error="Type a strong alpha-numeric eight character password with special characters."
        )
    
    if not validate_username(username):
        return render_template(
            "authentication/register.html",
            register_error="Only alphabets, numbers, (.), (-) and (_) in username."
        )
    
    u = User.query.filter_by(mobile=mobile).first()
    if u:
        return render_template(
            "authentication/register.html",
            register_error="This mobile number is associated with another account."
        )
    
    u = User.query.filter_by(email=email).first()
    if u:
        return render_template(
            "authentication/register.html",
            register_error="This email address is associated with another account."
        )
    
    u = User.query.filter_by(username=username).first()
    if u:
        return render_template(
            "authentication/register.html",
            register_error="This username is not available."
        )
    
    password = generate_password_hash(password1)
    code = str(random.randint(100000, 999999))

    session["registration"] = {
        "name": name,
        "mobile": mobile,
        "email": email,
        "username": username,
        "password": password,
        "code": code
    }

    content = getVerificationEmailContent(code)
    if sendemail(email, content):
        return redirect(url_for('authentication.verify_registration'))
    else:
        session["registration"].clear()
        session["registration"] = None
    
    return render_template(
        "authentication/register.html",
        register_error="Something went wrong. Please try again later."
    )


@bp.route("/register/verification/resendcode", methods=["POST", "GET"])
def resend_verification_code():
    if not session.get("registration"):
        return redirect(url_for('authentication.register'))
    
    code = str(random.randint(100000, 999999))
    content = getVerificationEmailContent(code)
    if sendemail(session["registration"]["email"], content):
        session["registration"]["code"] = code
        return redirect(url_for('authentication.verify_registration'))
    else:
        return redirect(url_for('authentication.register'))


@bp.route("/register/verification", methods=["POST", "GET"])
def verify_registration():
    if not session.get("registration"):
        return redirect(url_for('authentication.register'))

    if request.method == "GET":
        return render_template(
            "authentication/verification.html",
            email=session["registration"]["email"]
        )
    
    code = request.form.get("code")
    if not code:
        return render_template(
            "authentication/verification.html",
            email=session["registration"]["email"],
            verification_error="Enter the verification code."
        )

    if code != session["registration"]["code"]:
        return render_template(
            "authentication/verification.html",
            email=session["registration"]["email"],
            verification_error="Incorrect verification code."
        )
    
    admin = True if session["registration"]["email"] == envs.ADMINISTRATOR_EMAIL else False
    user = User(
        name=session["registration"]["name"],
        mobile=session["registration"]["mobile"],
        email=session["registration"]["email"],
        username=session["registration"]["username"],
        password=session["registration"]["password"],
        admin=admin
    )

    try:
        db.session.add(user)
        db.session.commit()
    except:
        email=session["registration"]["email"],
        session["registration"].clear()
        session["registration"] = None
        return render_template(
            "authentication/verification.html",
            email=email,
            verification_error="Something went wrong. Please try again later."
        )
    else:
        return redirect(url_for('authentication.confirmation'))


@bp.route("/confirmation")
def confirmation():
    if not session.get("registration"):
        return redirect(url_for('authentication.login'))
    
    session["registration"].clear()
    session["registration"] = None
    
    return render_template(
        "authentication/confirmation.html"
    )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('authentication.login'))


def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("administrator") == None:
            return redirect(url_for('authentication.login'))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("siteuser") == None:
            return redirect(url_for('authentication.login'))
        return f(*args, **kwargs)
    return decorated_function