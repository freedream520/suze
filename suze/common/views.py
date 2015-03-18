# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib

from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import login_user, logout_user
from forms import LoginForm, RegisterForm
from suze.common import BPCommon
from suze.models import User, Article


@BPCommon.route('/')
@BPCommon.route('/p/<int:page>/')
def index(page=1):
    pagination = Article.query.filter_by(deleted=False).order_by(Article.id.desc())\
            .paginate(page, per_page=10, error_out=True)
    return render_template('common/index.html', pagination=pagination)


@BPCommon.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = hashlib.md5(form.password.data).hexdigest()
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user)
            redirect_uri = request.args.get('redirect_uri', url_for('Common.index'))
            return redirect(redirect_uri)

    return render_template('common/login.html', form=form)


@BPCommon.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('Common.index', page=1))


@BPCommon.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        password = hashlib.md5(form.password.data).hexdigest()
        confirm_password = hashlib.md5(form.confirm_password.data).hexdigest()

        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return render_template('common/register.html', form=form)

        if password != confirm_password:
            flash('密码不一致')
            return render_template('common/register.html', form=form)

        user = User(username, password, '', '')
        user.save()
        login_user(user)

        return redirect(url_for('Common.index', page=1))

    return render_template('common/register.html', form=form)
