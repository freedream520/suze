# -*- coding: utf-8 -*-

import hashlib
import random
import os
import json

from suze.settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug import secure_filename
from flask import current_app

def check_permission(user, opt):
    return (user.permission & current_app.config['PERMISSION'][opt]) > 0

def set_permission(user, opt, value):
    if value <= 0:
        user.permission ^= current_app.config['PERMISSION'][opt]
    else:
        user.permission |= current_app.config['PERMISSION'][opt]

    user.save()

def show_permission(user):
    return [key for key, value in current_app.config['PERMISSION'].items() if user.permission & value > 0]

def list_permission():
    return [key for key, value in current_app.config['PERMISSION'].items()]

def no_permission(user):
    return [p for p in list_permission() if p not in show_permission(user)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_file(f):
    assert f and allowed_file(f.filename)
    filename = secure_filename(f.filename)
    name, type = filename.rsplit('.', 1)
    m = hashlib.md5()
    m.update(name)
    m.update(str(random.random()))
    name = m.hexdigest()
    filename = ".".join([name, type])
    f.save(os.path.join(UPLOAD_FOLDER, filename))

    return filename

def parse_json(json_string):
    return json.loads(json_string)

def parse_tags(tags):
    return '#'.join([x.tagname for x in tags])
