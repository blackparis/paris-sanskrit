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


@bp.route("/aphorisms", methods=["POST", "GET"])
def aphorisms():
    username = None if not session.get("siteuser") else session["siteuser"]["username"]
    if request.method == "GET":
        aphorisms_categories = get_aphorisms_categories()
        return render_template(
            "siteuser/basics/aphorisms.html",
            username=username,
            aphorisms_categories=aphorisms_categories
        )
    
    start = request.form.get("start")
    end = request.form.get("end")
    topic = request.form.get("topic")
    subtopic = request.form.get("subtopic")

    if not start or not end:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    try:
        start = int(start)
        end = int(end)
    except:
        return jsonify({"success": False, "message": "Invalid Form Data"})

    if topic and subtopic:
        aphorisms = Aphorism.query.filter_by(topic=topic).filter_by(subtopic=subtopic).order_by(Aphorism.number).slice(start, end).all()
    elif topic and not subtopic:
        aphorisms = Aphorism.query.filter_by(topic=topic).order_by(Aphorism.number).slice(start, end).all()
    elif subtopic and not topic:
        return jsonify({"success": False, "message": "Invalid Request"})
    else:
        aphorisms = Aphorism.query.order_by(Aphorism.number).slice(start, end).all()
    
    ap = []
    for a in aphorisms:
        ap.append({
            "number": a.number,
            "topic": a.topic,
            "subtopic": a.subtopic,
            "rule": a.rule
        })
    
    if len(ap) == 0:
        return jsonify({"success": True, "aphorisms": None})
    else:
        return jsonify({"success": True, "aphorisms": ap})


    




    



def get_aphorisms_categories():
    categories = {}

    aphorisms = Aphorism.query.all()
    for a in aphorisms:
        if a.topic not in categories:
            categories[a.topic] = set()
        (categories[a.topic]).add(a.subtopic)
    
    return categories