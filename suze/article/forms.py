# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, TextAreaField, HiddenField, validators, FileField, SelectField
from suze.models import Category


class CreateForm(Form):
    title = TextField('标题', [validators.DataRequired(), validators.Length(max=100)])
    html_content = TextAreaField('正文', [validators.DataRequired()])
    raw_content = HiddenField('正文', [validators.DataRequired()])
    cover = FileField('封面')
    category_id = SelectField('栏目', coerce=int)
