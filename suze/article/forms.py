# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, TextAreaField, validators


class CreateForm(Form):
    title = TextField('标题', [validators.DataRequired(), validators.Length(max=100)])
    tags = TextField('标签')
    content = TextAreaField('正文', [validators.DataRequired()])
