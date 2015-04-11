# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextAreaField, validators


class CommentForm(Form):
    content = TextAreaField('评论内容', [validators.DataRequired()])
