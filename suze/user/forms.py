# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, validators


class ProfileForm(Form):
    avatar = FileField('头像')
    mail = TextField('邮箱')
    homepage = TextField('主页')
    brief = TextAreaField('简介')


class PasswordForm(Form):
    old_password = PasswordField('旧密码', [validators.DataRequired()])
    new_password = PasswordField('新密码', [validators.DataRequired()])
    confirm_password = PasswordField('确认密码', [validators.DataRequired()])
