from flask import Blueprint, session, render_template, redirect, url_for, request, jsonify
from application.models import *
from application.authentication import login_required
from datetime import datetime
import random
#from application.sockets import *

bp = Blueprint("basics", __name__, url_prefix='/basics')

@bp.route("/")
def homepage():
    username = None if not session.get("siteuser") else session["siteuser"]["username"]
    return render_template(
        "siteuser/basics/homepage.html",
        username=username
    )


@bp.route("/aphorisms")
def aphorisms():
    username = None if not session.get("siteuser") else session["siteuser"]["username"]
    return render_template(
        "siteuser/basics/aphorisms.html",
        username=username
    )
