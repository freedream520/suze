# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import hashlib

from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import current_user
from forms import ProfileForm, PasswordForm
from suze.user import BPUser
from suze.models import User, Article
from suze.utils.common import save_file


@BPUser.route('/profile/<int:user_id>/', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('Common.index'))

    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        profile = json.loads(user.verbose) if user.verbose else dict()

        profile['mail'] = form.mail.data
        profile['homepage'] = form.homepage.data
        profile['brief'] = form.brief.data

        user.verbose = json.dumps(profile)

        f = request.files['avatar']
        if f:
            try:
                filename = save_file(f)
                user.avatar = filename
            except:
                pass

        user.save()

    profile = json.loads(user.verbose) if user.verbose else None
    return render_template('user/profile.html', user=user, form=form, profile=profile)


@BPUser.route('/password/<int:user_id>/', methods=['GET', 'POST'])
def password(user_id):
    user = User.query.get(user_id)
    if not user or (current_user != user):
        return redirect(url_for('Common.index'))

    form = PasswordForm(request.form)
    if request.method == 'POST':
        if form.validate():
            old_password = form.old_password.data
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            old_password = hashlib.md5(old_password).hexdigest()

            if old_password != user.password:
                flash('旧密码错误', 'error')
            elif new_password != confirm_password:
                flash('密码不一致', 'error')
            else:
                new_password = hashlib.md5(new_password).hexdigest()
                user.password = new_password
                user.save()
                flash('修改密码成功', 'success')
        else:
            flash('请按格式填写表单', 'error')

    return render_template('user/password.html', user=user, form=form)


@BPUser.route('/article/<int:user_id>/')
@BPUser.route('/article/<int:user_id>/<int:page>/')
def article(user_id, page=1):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('Common.index'))

    pagination = user.articles.order_by(Article.id.desc())\
            .paginate(page, per_page=10, error_out=True)

    return render_template('user/article.html', user=user, pagination=pagination)
