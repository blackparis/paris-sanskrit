from flask import Blueprint, session, render_template, redirect, url_for, request, jsonify
from application.models import *
from application.authentication import admin_login_required

bp = Blueprint("administrator", __name__, url_prefix='/administrator')

@bp.route("/")
@admin_login_required
def homepage():
    return render_template(
        "administrator/homepage.html"
    )


@bp.route("/aphorisms")
@admin_login_required
def aphorisms():
    topics = Topic.query.all()
    return render_template(
        "administrator/aphorisms.html",
        topics=topics
    )


@bp.route("/add_topic", methods=["POST"])
@admin_login_required
def add_topic():
    topic_name = request.form.get("topic_name")
    if not topic_name:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    topic_name = topic_name.strip()
    t = Topic.query.filter_by(name=topic_name).first()
    if t:
        return jsonify({"success": False, "message": "Already Exists"})
    
    t = Topic(name=topic_name)
    try:
        db.session.add(t)
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Unknown Error"})
    else:
        t = Topic.query.filter_by(name=topic_name).first()
        return jsonify({"success": True, "topic_name": t.name, "topic_id": t.id})


@bp.route("/add_subtopic", methods=["POST"])
@admin_login_required
def add_subtopic():
    topic_id = request.form.get("topic_id")
    subtopic_name = request.form.get("subtopic_name")

    if not topic_id or not subtopic_name:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    try:
        topic_id = int(topic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})

    t = Topic.query.get(topic_id)
    if not t:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    subtopic_name = subtopic_name.strip()
    st = SubTopic.query.filter_by(name=subtopic_name).filter_by(topic_id=topic_id).first()
    if st:
        return jsonify({"success": False, "message": "Already Exists"})
    
    st = SubTopic(
        topic_id=topic_id,
        name=subtopic_name
    )

    try:
        db.session.add(st)
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Database Error"})
    else:
        st = SubTopic.query.filter_by(name=subtopic_name).filter_by(topic_id=topic_id).first()
        return jsonify({"success": True, "subtopic_name": st.name, "subtopic_id": st.id, "topic_id": topic_id})


@bp.route("/get_topics")
def get_topics():
    topics = Topic.query.all()
    tp = []
    for t in topics:
        tp.append({
            "id": t.id,
            "name": t.name
        })
    
    if len(tp) == 0:
        return jsonify({"success": False, "message": "No Topics"})
    
    return jsonify({"success": True, "topics": tp})


@bp.route("/GetSubTopics", methods=["POST"])
def GetSubTopics():
    subtopic_id = request.form.get("subtopic_id")
    if not subtopic_id:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    try:
        subtopic_id = int(subtopic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    st = SubTopic.query.get(subtopic_id)
    if not st:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    subtopics = SubTopic.query.filter_by(topic_id=st.topic_id).all()
    response = []
    for s in subtopics:
        response.append({
            "id": s.id,
            "name": s.name
        })
    
    return jsonify({"success": True, "subtopics": response})


@bp.route("/get_subtopic", methods=["POST"])
def get_sub_topic():
    topic_id = request.form.get("topic_id")
    if not topic_id:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    try:
        topic_id = int(topic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    t = Topic.query.get(topic_id)
    if not t:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    subtopics = []
    stps = t.subtopics

    for stp in stps:
        subtopics.append({
            "subtopic_id": stp.id,
            "subtopic_name": stp.name,
            "topic_id": stp.topic_id
        })

    return jsonify({"success": True, "topic_id": topic_id, "subtopics": subtopics, "topic_name": t.name})


@bp.route("/get_rules", methods=["POST"])
def get_rules():
    subtopic_id = request.form.get("subtopic_id")
    if not subtopic_id:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    try:
        subtopic_id = int(subtopic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    st = SubTopic.query.get(subtopic_id)
    if not st:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    rules = Aphorism.query.filter_by(subtopic_id=subtopic_id).order_by(Aphorism.number).all()
    aphorisms = []
    for rule in rules:
        aphorisms.append({
            "id": rule.id,
            "number": rule.number,
            "rule": rule.rule,
            "subtopic_id": rule.subtopic_id
        })

    return jsonify({"success": True, "topic_name": st.topic.name, "subtopic_name": st.name, "aphorisms": aphorisms, "subtopic_id": subtopic_id})


@bp.route("/add_aphorism", methods=["POST"])
@admin_login_required
def add_aphorism():
    subtopic_id = request.form.get("subtopic_id")
    number = request.form.get("number")
    aphorism = request.form.get("aphorism")

    if not subtopic_id or not number or not aphorism:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    aphorism = aphorism.strip()
    number = number.strip()
    
    try:
        subtopic_id = int(subtopic_id)
        number = int(number)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    st = SubTopic.query.get(subtopic_id)
    if not st:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    r = Aphorism.query.filter_by(number=number).first()
    if r:
        return jsonify({"success": False, "message": "Rule Number Already Exists"})
    
    r = Aphorism.query.filter_by(subtopic_id=subtopic_id).filter_by(rule=aphorism).first()
    if r:
        return jsonify({"success": False, "message": "Rule Already Exists"})
    
    r = Aphorism(
        number=number,
        subtopic_id=subtopic_id,
        rule=aphorism
    )

    try:
        db.session.add(r)
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Database Error"})
    else:
        r = Aphorism.query.filter_by(number=number).first()
        return jsonify({
            "success": True,
            "rule_id": r.id,
            "number": r.number,
            "rule": r.rule
        })


@bp.route("/edit_topic", methods=["POST"])
@admin_login_required
def edit_topic():
    topic_id = request.form.get("topic_id")
    topic_name = request.form.get("TopicName")

    if not topic_id or not topic_name:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    topic_name = topic_name.strip()
    try:
        topic_id = int(topic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    t = Topic.query.filter_by(name=topic_name).first()
    if t:
        return jsonify({"success": False, "message": "Already Exists"})
    
    t = Topic.query.get(topic_id)
    if not t:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    t.name = topic_name
    try:
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Database Error"})
    else:
        return jsonify({"success": True, "topic_name": topic_name})


@bp.route("/edit_subtopic", methods=["POST"])
@admin_login_required
def edit_subtopic():
    subtopic_id = request.form.get("subtopic_id")
    SubTopicName = request.form.get("SubTopicName")
    topic_id = request.form.get("topic_id")
    new_topic_id = request.form.get("new_topic_id")

    if not subtopic_id or not SubTopicName or not topic_id:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    try:
        subtopic_id = int(subtopic_id)
        topic_id = int(topic_id)
        new_topic_id = int(new_topic_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    t = Topic.query.get(new_topic_id)
    if not t:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    SubTopicName = SubTopicName.strip()
    st = SubTopic.query.filter_by(topic_id=new_topic_id).filter_by(name=SubTopicName).first()
    if st:
        return jsonify({"success": False, "message": "Already Exists"})
    
    st = SubTopic.query.get(subtopic_id)
    if not st:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    st.topic_id = new_topic_id
    st.name = SubTopicName

    try:
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Database Error"})
    else:
        return jsonify({"success": True})


@bp.route("/edit_rule", methods=["POST"])
@admin_login_required
def edit_rule():
    new_subtopic_id = request.form.get("new_subtopic_id")
    new_rule_number = request.form.get("new_rule_number")
    new_rule = request.form.get("new_rule")
    rule_id = request.form.get("rule_id")

    if not new_subtopic_id or not new_rule_number or not new_rule or not rule_id:
        return jsonify({"success": False, "message": "Incomplete Form Data"})
    
    new_rule = new_rule.strip()
    try:
        new_subtopic_id = int(new_subtopic_id)
        new_rule_number = int(new_rule_number)
        rule_id = int(rule_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid Form Data"})
    
    st = SubTopic.query.get(new_subtopic_id)
    if not st:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    rule = Aphorism.query.get(rule_id)
    if not rule:
        return jsonify({"success": False, "message": "Invalid Request"})
    
    if rule.number != new_rule_number:
        r = Aphorism.query.filter_by(number=new_rule_number).first()
        if r:
            return jsonify({"success": False, "message": "Rule Number Already Exists"})
    else:
        r = Aphorism.query.filter_by(subtopic_id=new_subtopic_id).filter_by(rule=new_rule).first()
        if r:
            return jsonify({"success": False, "message": "Rule Already Exists"})
    
    rule.number = new_rule_number
    rule.subtopic_id = new_subtopic_id
    rule.rule = new_rule

    try:
        db.session.commit()
    except:
        return jsonify({"success": False, "message": "Database Error"})
    else:
        return jsonify({"success": True})