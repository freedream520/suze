# -*- coding: utf-8 -*-

import hashlib
import random
import os
import json

from suze.settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug import secure_filename


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
