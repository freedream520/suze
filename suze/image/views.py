# -*- coding: utf-8 -*-

from flask import request, current_app, send_from_directory, redirect, url_for
# from flask.ext.login import login_required
from suze.utils.common import save_file
from suze.image import BPImage


@BPImage.route('/create/', methods=['POST'])
def create():
    f = request.files['image']
    save_file(f)
    return redirect(url_for('Common.index', page=1))


@BPImage.route('/retrieve/<imagename>/', methods=['GET'])
def retrieve(imagename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], imagename)
