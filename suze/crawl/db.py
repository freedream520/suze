# -*- coding: utf-8 -*-

import torndb

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASS = "britten"
MYSQL_DB = "wemedia_crawl"

DB = torndb.Connection(
'%s:%s' % (MYSQL_HOST, str(MYSQL_PORT)),
    MYSQL_DB,
    MYSQL_USER,
    MYSQL_PASS,
)
