from flask import Blueprint, session, render_template, redirect, url_for, request, jsonify
from application.models import *
from application.authentication import login_required
from datetime import datetime
import random
#from application.sockets import *

bp = Blueprint("siteuser", __name__)

@bp.route("/")
def homepage():
    username = None if not session.get("siteuser") else session["siteuser"]["username"]
    return render_template(
        "siteuser/homepage.html",
        username=username
    )