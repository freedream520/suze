# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import render_template, url_for, redirect, request
from flask.ext.login import login_required, current_user
from forms import CreateForm
from suze.article import BPArticle
from suze.models import Article, Tag
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
    if request.method == 'POST' and form.validate():
        title = form.title.data
        tags = form.tags.data
        html_content = form.html_content.data
        raw_content = form.raw_content.data
        brief = raw_content[:100]

        tags = sorted(filter(lambda x: len(x), map(lambda x: x.strip(), list(set(tags.split("#"))))))

        def create_tag(tagname):
            t = Tag(tagname)
            t.save()

            return t

        tags = map(create_tag, tags)
        article = Article(current_user.id, title, brief, tags, raw_content, html_content)
        article.save()

        return redirect(url_for('Article.retrieve', article_id=article.id))

    return render_template('article/create.html', form=form)


@BPArticle.route('/update/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def update(article_id):
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for('Common.index'))

    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        tags = form.tags.data
        html_content = form.html_content.data
        raw_content = form.raw_content.data
        brief = raw_content[:100]

        tags = sorted(filter(lambda x: len(x), map(lambda x: x.strip(), list(set(tags.split("#"))))))

        def create_tag(tagname):
            t = Tag(tagname)
            t.save()

            return t

        tags = map(create_tag, tags)

        article.title = title
        article.brief = brief
        article.tags = tags
        article.raw_content = raw_content
        article.html_content = html_content

        article.update()

        return redirect(url_for('Article.retrieve', article_id=article.id))

    tags = '#'.join([x.tagname for x in article.tags.all()])

    return render_template('article/update.html', form=form, article=article, tags=tags)


@BPArticle.route('/delete/<int:article_id>/', methods=['GET'])
@login_required
def delete(article_id):
    article = Article.query.get(article_id)
    if article and current_user == article.author:
        article.delete()

    return redirect(url_for('Common.index'))
