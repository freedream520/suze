# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, TextAreaField, HiddenField, validators


class CreateForm(Form):
    title = TextField('标题', [validators.DataRequired(), validators.Length(max=100)])
    tags = TextField('标签')
    html_content = TextAreaField('正文', [validators.DataRequired()])
    raw_content = HiddenField('正文', [validators.DataRequired()])
