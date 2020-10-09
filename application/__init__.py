import os

from flask import Flask, render_template
from application.config import Config
from application.models import *
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
#from application.sockets import socketio

from application import administrator, authentication, siteuser, basics


def create_app():
    application = Flask(__name__)

    application.config.from_object(Config)

    Session(application)
    csrf = CSRFProtect(application)
    db.init_app(application)
    #socketio.init_app(application)

    application.register_blueprint(authentication.bp)
    application.register_blueprint(siteuser.bp)
    application.register_blueprint(administrator.bp)
    application.register_blueprint(basics.bp)

    application.add_url_rule('/', endpoint='homepage')

    @application.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

    return application