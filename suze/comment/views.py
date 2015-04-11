# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

from forms import CommentForm
from flask import url_for, request, redirect, flash
from flask.ext.login import login_required, current_user
from suze.comment import BPComment
from suze.models import Article, Comment, User
from suze.utils.common import check_permission


@BPComment.route('/create/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def create(article_id):
    if not check_permission(current_user, 'comment'):
        flash('你没有权限')
        return redirect(url_for('Article.retrieve', article_id=article_id))
    form = CommentForm(request.form)
    if form.validate():
        article = Article.query.get(article_id)
        raw_content = form.content.data
        def _replace(matched):
            user = User.query.filter_by(username=matched.group('username')).first()
            return "<a href=" + url_for('User.profile', user_id=user.id) + ">@{username}</a>:"\
                    .format(username=matched.group('username'))
        html_content = re.sub(r'@(?P<username>[^:]+):', _replace, raw_content)
        comment = Comment(article.id, current_user.id, html_content)
        comment.save()

    return redirect(url_for('Article.retrieve', article_id=article_id))


@BPComment.route('/delete/<int:article_id>/<int:comment_id>/')
@login_required
def delete(article_id, comment_id):
    article = Article.query.get(article_id)
    comment = Comment.query.get(comment_id)

    if not article:
        return redirect(url_for('Comment.index'))

    if comment and ((comment.author == current_user) or (article.author == current_user)):
        comment.delete()

    return redirect(url_for('Article.retrieve', article_id=article.id))
