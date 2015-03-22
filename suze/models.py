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
    verbose = db.Column(db.TEXT)

    def __init__(self, username, password, avatar, verbose):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.verbose = verbose

    def save(self):
        db.session.add(self)
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
    tags = db.relationship('Tag', backref='article', lazy='dynamic')
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __init__(self, author_id, title, brief, tags, raw_content, html_content):
        self.author_id = author_id
        self.title = title
        self.brief = brief
        self.tags = tags
        self.raw_content = raw_content
        self.html_content = html_content
        self.created = time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        self.deleted = True
        self.save()


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(80))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, tagname):
        self.tagname = tagname

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
