from flask import Blueprint, session, render_template, redirect, url_for, request, jsonify
from application.models import *
from application.authentication import admin_login_required

bp = Blueprint("administrator", __name__, url_prefix='/administrator')

@bp.route("/")
@admin_login_required
def homepage():
    return "hello, admin!"