# -*- coding: utf-8 -*-

import settings

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from utils.common import parse_json, parse_tags

db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    setup_db(app)
    setup_blueprint(app)
    setup_login(app)
    setup_global(app)

    return app

def setup_global(app):
    @app.before_request
    def before_request():
        g.parse_json = parse_json
        g.parse_tags = parse_tags

def setup_blueprint(app):
    from common import BPCommon
    from image import BPImage
    from article import BPArticle
    from comment import BPComment
    from user import BPUser

    app.register_blueprint(BPCommon, url_prefix='')
    app.register_blueprint(BPImage, url_prefix='/image')
    app.register_blueprint(BPArticle, url_prefix='/article')
    app.register_blueprint(BPComment, url_prefix='/comment')
    app.register_blueprint(BPUser, url_prefix='/user')

def setup_db(app):
    global db
    db = SQLAlchemy(app)
    import models
    # db.drop_all()
    db.create_all()

def setup_login(app):
    from models import User
    login_manager = LoginManager()
    login_manager.login_view = 'Common.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(userid)
