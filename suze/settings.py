# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join

DEBUG = True
SECRET_KEY = 'u\x9e\xd1\xcf\xba\x0b\xea[\xf0wO\xef\xefM\x8b^7!\xb7`\x16\x1c\xc9\xf4'
SQLALCHEMY_DATABASE_URI = 'mysql://root:britten@localhost/wemedia'
PER_PAGE = 10
# SERVER_NAME = 'blog.liqueurz.me'
UPLOAD_FOLDER = join(dirname(abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
SERVER_NAME = 'localhost:8080'
