# -*- coding: utf-8 -*-

import json

from flask import request, current_app, send_from_directory, redirect, url_for
# from flask.ext.login import login_required
from suze.utils.common import save_file
from suze.image import BPImage


@BPImage.route('/create/', methods=['POST'])
def create():
    f = request.files['upfile']
    name = save_file(f)
    data = {'url':url_for('.retrieve', imagename=name), 'state':'SUCCESS', 'title':name, 'original':name}
    print json.dumps(data)
    return json.dumps(data)


@BPImage.route('/retrieve/<imagename>/', methods=['GET'])
def retrieve(imagename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], imagename)
