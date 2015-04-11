# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, validators, FileField, IntegerField, HiddenField


class CarouselForm(Form):
    order_num = IntegerField('序号', [validators.DataRequired()])
    url = TextField('链接', [validators.DataRequired()])
    cover = FileField('封面')
    title = TextField('标题', [validators.DataRequired()])
    brief = TextField('摘要', [validators.DataRequired()])

class CarouselUpdateForm(Form):
    carousel_id = HiddenField('', [validators.DataRequired()])
    order_num = IntegerField('序号', [validators.DataRequired()])
    url = TextField('链接', [validators.DataRequired()])
    cover = FileField('封面')
    title = TextField('标题', [validators.DataRequired()])
    brief = TextField('摘要', [validators.DataRequired()])

class CategoryForm(Form):
    category_name = TextField('目录名', [validators.DataRequired()])

class CategoryUpdateForm(Form):
    category_id = HiddenField('', [validators.DataRequired()])
    category_name = TextField('目录名', [validators.DataRequired()])
