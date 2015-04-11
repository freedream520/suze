# -*- coding: utf-8 -*-

import time

from flask.ext.login import UserMixin
from suze import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column('password', db.String(32))
    avatar = db.Column(db.String(80))
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    # flows = db.relationship('Flow', backref='user', lazy='dynamic', remote_side=['user_id'])
    verbose = db.Column(db.TEXT)
    permission = db.Column(db.Integer, default=0b110)

    def __init__(self, username, password, avatar, verbose):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.verbose = verbose

    def save(self):
        db.session.add(self)
        db.session.commit()


class Flow(db.Model):
    __tablename__ = 'flow'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    flower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __init__(self, user_id, flower_id):
        self.user_id = user_id
        self.flower_id = flower_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    html_content = db.Column(db.TEXT)
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.TIMESTAMP)

    def __init__(self, article_id, author_id, html_content):
        self.article_id = article_id
        self.author_id = author_id
        self.html_content = html_content
        self.created = time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.deleted = True
        self.save()


class Favor(db.Model):
    __tablename__ = 'favor'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True)

    def __init__(self, user_id, article_id):
        self.user_id = user_id
        self.article_id = article_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80))
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __init__(self, category_name):
        self.category_name = category_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    brief = db.Column(db.TEXT)
    raw_content = db.Column(db.TEXT)
    html_content = db.Column(db.TEXT)
    deleted = db.Column(db.Boolean, default=False)
    created = db.Column(db.TIMESTAMP)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    likes = db.relationship('Favor', backref='article', lazy='dynamic')
    clicks = db.Column(db.Integer, default=0)
    cover = db.Column(db.String(80))

    def __init__(self, author_id, title, brief, raw_content, html_content, category_id):
        self.author_id = author_id
        self.title = title
        self.brief = brief
        self.raw_content = raw_content
        self.html_content = html_content
        self.created = time.strftime('%Y-%m-%d %H:%M:%S')
        self.category_id = category_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.deleted = True
        self.save()

    def recover(self):
        self.deleted = False
        self.save()


class Carousel(db.Model):
    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.Integer, default=0)
    url = db.Column(db.TEXT)
    cover = db.Column(db.String(80))
    title = db.Column(db.String(80))
    brief = db.Column(db.String(80))
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, order_num, url, cover, title, brief):
        self.order_num = order_num
        self.url = url
        self.cover = cover
        self.title = title
        self.brief = brief

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.deleted = True
        self.save()

class Traffic(db.Model):
    __tablename__ = 'traffic'

    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __init__(self, hour, count):
        self.hour = hour
        self.count = count

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
