# -*- coding: utf-8 -*-

import settings
import random

from flask import Flask, g, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from utils.common import parse_json, parse_tags, check_permission, show_permission, list_permission,\
        no_permission

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
    from suze.common.forms import LoginForm, RegisterForm
    from suze.models import Article, User, Flow
    def is_flowed(user_id, flower_id):
        return Flow.query.filter_by(user_id=user_id, flower_id=flower_id).first() is not None

    @app.before_request
    def before_request():
        g.parse_json = parse_json
        g.parse_tags = parse_tags
        g.check_permission = check_permission
        g.show_permission = show_permission
        g.list_permission = list_permission
        g.no_permission = no_permission
        g.is_flowed = is_flowed
        g.login_form = LoginForm()
        g.register_form = RegisterForm()
        sql = ('select count(f.user_id) as count, '
        'f.article_id as article_id from favor as f group by article_id order by count desc limit 9')
        g.hot_articles = [Article.query.get(row[1]) for row in db.engine.execute(sql)]
        users = User.query.all()
        random.shuffle(users)
        g.recommend_users = users[:5]

def setup_blueprint(app):
    from common import BPCommon
    from image import BPImage
    from article import BPArticle
    from comment import BPComment
    from user import BPUser
    from admin import BPAdmin

    app.register_blueprint(BPCommon, url_prefix='')
    app.register_blueprint(BPImage, url_prefix='/image')
    app.register_blueprint(BPArticle, url_prefix='/article')
    app.register_blueprint(BPComment, url_prefix='/comment')
    app.register_blueprint(BPUser, url_prefix='/user')
    app.register_blueprint(BPAdmin, url_prefix='/admin')

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
