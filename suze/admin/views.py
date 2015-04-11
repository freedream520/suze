# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import random
import json

from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import login_user, logout_user, current_user
from suze.admin import BPAdmin
from forms import CarouselForm, CarouselUpdateForm, CategoryForm, CategoryUpdateForm
from suze.utils.common import save_file, list_permission, set_permission, check_permission
from suze.models import Carousel, Article, User, Category, Traffic
from suze import db
from datetime import datetime


@BPAdmin.route('/analyse/', methods=['GET', 'POST'])
@BPAdmin.route('/', methods=['GET', 'POST'])
def analyse():
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    return render_template('admin/analyse.html')

@BPAdmin.route('/analyse/traffic/', methods=['GET'])
def analyse_traffic():
    def foo(n):
        s = [i for i in range(24)]
        s = s[n:24] + s[0:n]
        count = []
        for h in s:
            c = Traffic.query.filter_by(hour=h).first()
            count.append(c.count if c else 0)
        return {'labels':[str(i) + '时' for i in s],'traffic':count}
    return json.dumps(foo(datetime.now().hour))

@BPAdmin.route('/analyse/submit/', methods=['GET'])
def analyse_submit():
    sql = 'select count(*) as count from article group by author_id'
    data = [0, 0, 0, 0]
    for row in db.engine.execute(sql):
        if row[0] < 10:
            data[0] += 1
        elif row[0] < 100:
            data[1] += 1
        elif row[0] < 500:
            data[2] += 1
        elif row[0] >= 500:
            data[3] += 1

    return json.dumps(data)

@BPAdmin.route('/analyse/interest/', methods=['GET'])
def analyse_interest():
    sql = ('select sum(article.clicks) as count, category.category_name as category'
    ' from article, category where article.category_id=category.id'
    ' group by category.category_name')

    data = {
            'category':[row['category'] for row in db.engine.execute(sql)],
            'count':[int(row['count']) for row in db.engine.execute(sql)],
            }
    return json.dumps(data)

@BPAdmin.route('/carousel/', methods=['GET', 'POST'])
def carousel():
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    form = CarouselForm(request.form)
    if form.validate() and request.method == 'POST':
        order_num = form.order_num.data
        url = form.url.data
        title = form.title.data
        brief = form.brief.data
        cover = ''
        f = request.files['cover']
        if f:
            cover = save_file(f)
        c = Carousel(order_num, url, cover, title, brief)
        c.save()
    kwargs = dict(
        carousel_form=form,
        carousel_update_form=CarouselUpdateForm(),
        carousels=Carousel.query.filter_by(deleted=False).order_by(Carousel.order_num).all(),
    )
    return render_template('admin/carousel.html', **kwargs)

@BPAdmin.route('/carousel/delete/<int:carousel_id>/', methods=['GET'])
def delete_carousel(carousel_id):
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    carousel = Carousel.query.get(carousel_id)
    carousel.delete()
    kwargs = dict(
        carousel_form=CarouselForm(),
        carousel_update_form=CarouselUpdateForm(),
        carousels=Carousel.query.filter_by(deleted=False).order_by(Carousel.order_num).all(),
    )
    return render_template('admin/carousel.html', **kwargs)

@BPAdmin.route('/carousel/update/', methods=['POST'])
def update_carousel():
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    form = CarouselUpdateForm(request.form)
    if form.validate() and request.method == 'POST':
        carousel_id = form.carousel_id.data
        c = Carousel.query.get(carousel_id)
        c.order_num = form.order_num.data
        c.url = form.url.data
        c.title = form.title.data
        c.brief = form.brief.data
        f = request.files['cover']
        if f:
            c.cover = save_file(f)
        c.update()

    kwargs = dict(
        carousel_form=CarouselForm(),
        carousel_update_form=form,
        carousels=Carousel.query.filter_by(deleted=False).order_by(Carousel.order_num).all(),
    )
    return render_template('admin/carousel.html', **kwargs)

@BPAdmin.route('/article/', methods=['GET', 'POST'])
@BPAdmin.route('/article/<int:page>/', methods=['GET', 'POST'])
def article(page=1):
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    pagination = Article.query.order_by(Article.id.desc())\
            .paginate(page, per_page=30, error_out=True)
    return render_template('admin/article.html', pagination=pagination)

@BPAdmin.route('/category/', methods=['GET', 'POST'])
def category():
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))

    category_form = CategoryForm(request.form)
    if category_form.validate():
        c = Category(category_form.category_name.data)
        c.save()

    kwargs = dict(
        category_form=category_form,
        categorys=Category.query.all(),
        category_update_form=CategoryUpdateForm(),
    )
    return render_template('admin/category.html', **kwargs)

@BPAdmin.route('/category/update/', methods=['GET', 'POST'])
def update_category():
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))

    category_update_form = CategoryUpdateForm(request.form)
    if category_update_form.validate():
        c = Category.query.get(category_update_form.category_id.data)
        c.category_name = category_update_form.category_name.data
        c.save()

    kwargs = dict(
        category_update_form=category_update_form,
        category_form=CategoryForm(),
        categorys=Category.query.all(),
    )
    return render_template('admin/category.html', **kwargs)

@BPAdmin.route('/permission/', methods=['GET', 'POST'])
@BPAdmin.route('/permission/<int:page>/', methods=['GET', 'POST'])
def permission(page=1):
    if not check_permission(current_user, 'admin'):
        flash('你没有权限')
        return redirect(url_for('Common.index'))
    if request.method == 'POST':
        user = User.query.get(request.form['user_id'])
        for p in list_permission():
            if not request.form.get(p, False):
                set_permission(user, p, 0)
            else:
                set_permission(user, p, 1)

    pagination = User.query.order_by(User.id.desc())\
            .paginate(page, per_page=30, error_out=True)
    return render_template('admin/permission.html', pagination=pagination)
