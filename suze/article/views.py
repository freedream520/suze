# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_required, current_user
from forms import CreateForm
from suze.article import BPArticle
from suze.models import Article, Category, Traffic
from suze.comment.forms import CommentForm
from suze.utils.common import save_file, check_permission
from datetime import datetime

@BPArticle.route('/retrieve/<int:article_id>/')
def retrieve(article_id):
    hour = datetime.now().hour
    t = Traffic.query.filter_by(hour=hour).first()
    if t is None:
        t = Traffic(hour, 0)
        t.save()
    t.count += 1
    t.update()
    article = Article.query.get(article_id)
    article.clicks += 1
    article.update()
    if (not article) or article.deleted:
        return redirect(url_for('Common.index', page=1))

    form = CommentForm()
    return render_template('article/retrieve.html', article=article, comment_form=form)


@BPArticle.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if not check_permission(current_user, 'article'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    form = CreateForm(request.form)
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if request.method == 'POST' and form.validate():
        title = form.title.data
        html_content = form.html_content.data
        raw_content = form.raw_content.data
        category_id = form.category_id.data
        brief = raw_content[:100]

        article = Article(current_user.id, title, brief, raw_content, html_content, category_id)

        f = request.files['cover']
        if f:
            try:
                article.cover = save_file(f)
            except Exception, e:
                pass

        article.save()

        return redirect(url_for('Common.index'))

    return render_template('article/create.html', form=form)


@BPArticle.route('/update/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def update(article_id):
    article = Article.query.get(article_id)
    form = CreateForm(request.form)
    form.category_id.choices = [(c.id, c.category_name) for c in Category.query.all()]
    if form.validate():
        title = form.title.data
        html_content = form.html_content.data
        raw_content = form.raw_content.data
        category_id = form.category_id.data
        brief = raw_content[:100]
        category_id = form.category_id.data

        article.title = title
        article.brief = brief
        article.raw_content = raw_content
        article.html_content = html_content
        article.category_id = category_id

        f = request.files['cover']
        if f:
            try:
                article.cover = save_file(f)
            except Exception, e:
                pass

        article.update()

        return redirect(url_for('Article.retrieve', article_id=article.id))

    kwargs = dict(
        form=form,
        article=article,
    )
    return render_template('article/update.html', **kwargs)


@BPArticle.route('/delete/<int:article_id>/', methods=['GET'])
@login_required
def delete(article_id):
    article = Article.query.get(article_id)
    if article:
        article.delete()

    return 'SUCCESS'

@BPArticle.route('/recover/<int:article_id>/', methods=['GET'])
@login_required
def recover(article_id):
    article = Article.query.get(article_id)
    if article:
        article.recover()

    return 'SUCCESS'
