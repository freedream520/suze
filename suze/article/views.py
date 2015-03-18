# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import render_template, url_for, redirect, request
from flask.ext.login import login_required
from forms import CreateForm
from suze.article import BPArticle
from suze.models import Article
from suze.comment.forms import CommentForm

@BPArticle.route('/retrieve/<int:article_id>/')
def retrieve(article_id):
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for('Common.index', page=1))

    form = CommentForm()
    return render_template('article/retrieve.html', article=article, form=form)


@BPArticle.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm(request.form)
    return render_template('article/create.html', form=form)
