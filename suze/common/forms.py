# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('用户名', [validators.DataRequired()])
    password = PasswordField('密码', [validators.DataRequired()])


class RegisterForm(Form):
    username = TextField('用户名', [validators.DataRequired()])
    password = PasswordField('密码', [validators.DataRequired()])
    confirm_password = PasswordField('确认密码', [validators.DataRequired()])
