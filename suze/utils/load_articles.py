# -*- coding: utf-8 -*-

"""
文章爬虫数据迁移脚本
"""

import MySQLdb
import time
import random

data = []


def gen_source_conn():
    return MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='britten',
                           db='wemedia_crawl',
                           charset='utf8')


def gen_dist_conn():
    return MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='britten',
                           db='wemedia',
                           charset='utf8')


def query(name, code):
    dist_conn = gen_dist_conn()
    source_conn = gen_source_conn()
    dist_cursor = dist_conn.cursor()
    source_cursor = source_conn.cursor()
    sql = 'select id from user where username=%s limit 1'
    dist_cursor.execute(sql, name)
    user_id = dist_cursor.fetchall()[0][0]
    created = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = 'select title, brief, content from article where code=%s'
    source_cursor.execute(sql, code)
    rs = source_cursor.fetchall()
    rs = map(lambda x: list(x), rs)
    for row in rs:
        row.append(created)
        row.append(user_id)
        row.append(0)

    data.extend(rs)

    dist_conn.close()
    source_conn.close()


def insert(data):
    random.shuffle(data)
    dist_conn = gen_dist_conn()
    dist_cursor = dist_conn.cursor()
    sql = 'insert into article(title, brief, html_content, created, author_id, deleted) values (%s, %s, %s, %s, %s, %s)'
    dist_cursor.executemany(sql, data)
    dist_conn.commit()
    dist_conn.close()


def drop():
    sql = 'delete from article'
    dist_conn = gen_dist_conn()
    dist_cursor = dist_conn.cursor()
    dist_cursor.execute(sql)
    dist_conn.commit()


def run():
    drop()
    query('知道日报', 'zdrb')
    query('虎嗅网', 'hx')
    query('36氪', '36kr')
    insert(data)


if __name__ == '__main__':
    run()
