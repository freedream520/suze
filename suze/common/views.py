# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import random

from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm, SearchForm
from suze.common import BPCommon
from suze.models import User, Article, Favor, Carousel, Category, Flow
from suze import db
from suze.utils.common import check_permission


@BPCommon.route('/')
@BPCommon.route('/p/<int:page>/')
def index(page=1):
    pagination = Article.query.filter_by(deleted=False).order_by(Article.id.desc())\
            .paginate(page, per_page=10, error_out=True)
    kwargs = dict(
        pagination=pagination,
        categorys=Category.query.all(),
        carousels = Carousel.query.filter_by(deleted=False).order_by(Carousel.order_num).all()
    )
    return render_template('common/index.html', **kwargs)

@BPCommon.route('/category/<int:category_id>/')
@BPCommon.route('/category/<int:category_id>/<int:page>/')
def category(category_id, page=1):
    pagination = Article.query.filter_by(deleted=False, category_id=category_id).order_by(Article.id.desc())\
            .paginate(page, per_page=10, error_out=True)

    kwargs = dict(
        pagination=pagination,
        selected_category=Category.query.get(category_id),
        categorys=Category.query.all(),
    )
    return render_template('common/index.html', **kwargs)

@BPCommon.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = hashlib.md5(form.password.data).hexdigest()
        user = User.query.filter_by(username=username, password=password).first()
        redirect_uri = request.args.get('redirect_uri', url_for('Common.index'))

        if user is not None:
            login_user(user)
        else:
            flash('登录失败')

        return redirect(redirect_uri)

    return redirect(url_for('Common.index'))


@BPCommon.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('Common.index', page=1))


@BPCommon.route('/register/', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        password = hashlib.md5(form.password.data).hexdigest()
        confirm_password = hashlib.md5(form.confirm_password.data).hexdigest()

        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('Common.index'))

        if password != confirm_password:
            flash('密码不一致')
            return redirect(url_for('Common.index'))

        user = User(username, password, 'user.jpg', '')
        user.save()
        login_user(user)

        return redirect(url_for('Common.index'))

    return redirect(url_for('Common.index'))


@BPCommon.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    articles = None
    if form.validate() and request.method == 'POST':
        title = form.title.data
        articles = Article.query.filter(Article.deleted == False, Article.raw_content.contains(title)).order_by(Article.id.desc())

    return render_template('common/search.html', articles=articles)


@BPCommon.route('/like/<int:user_id>/<int:article_id>/')
def like(user_id, article_id):
    user = User.query.get(user_id)
    article = Article.query.get(article_id)
    if (not user) or (not article):
        return '0'

    try:
        f = Favor(user.id, article.id)
        f.save()
        return '1'
    except:
        return '0'

@BPCommon.route('/myflow/', methods=['GET'])
@BPCommon.route('/myflow/<int:page>/', methods=['GET'])
@login_required
def myflow(page=1):
    users = [User.query.get(f.user_id) for f in Flow.query.filter_by(flower_id=current_user.id)]
    articles = []
    for user in users:
        articles.extend(user.articles.all())
    article_ids = [article.id for article in articles]
    pagination = Article.query.filter(Article.id.in_(article_ids), Article.deleted == False).order_by(Article.id.desc())\
            .paginate(page, per_page=10, error_out=True)
    kwargs = dict(
        pagination=pagination,
        categorys=Category.query.all(),
        carousels=Carousel.query.filter_by(deleted=False).order_by(Carousel.order_num).all(),
        myflow=True,
    )
    return render_template('common/index.html', **kwargs)

@BPCommon.route('/flow/', methods=['POST'])
def flow():
    user_id = request.form['user_id']
    flower_id = request.form['flower_id']
    f = Flow(user_id, flower_id)
    f.save()

    return 'SUCCESS'

@BPCommon.route('/unflow/', methods=['POST'])
def unflow():
    user_id = request.form['user_id']
    flower_id = request.form['flower_id']
    f = Flow.query.filter_by(user_id=user_id, flower_id=flower_id).first()
    f.delete()

    return 'SUCCESS'
