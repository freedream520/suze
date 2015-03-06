# -*- coding: utf-8 -*-

"""
虎嗅爬虫脚本
"""

import gevent
import gevent.monkey
gevent.monkey.patch_socket()
import time
import MySQLdb
import sys

from lxml import etree
from db import DB
from settings import CRAWL_URLS
from utils import retrieve

data = [[]]


def text(i, url, params):
    """
    抓取保存文章正文
    """
    content = retrieve(url, params)
    tree = etree.HTML(content)
    t = tree.xpath("//div[@id='article_content']/*")
    _content = ''.join(map(lambda x: etree.tostring(x, encoding='utf-8'), t))
    data[i].append(_content)


def profile(url, params):
    """
    抓取保存封面，标题，摘要
    """
    content = retrieve(url, params)
    tree = etree.HTML(content)

    for x in tree.xpath("//div[@class='clearfix mod-b mod-art']"):
        cover = x.find('a/img').attrib['src']
        title = x.find("div/h3/a").text
        url = 'http://www.huxiu.com' + x.find("div/h3/a").attrib['href']
        brief = x.find("div/div[2]").text
        author = '虎嗅网'
        code = 'hx'

        data.append([url, cover, title, brief, author, code])


def drop():
    sql = 'DELETE FROM article WHERE code=%s'
    DB.update(sql, 'hx')


def run():
    """
    启动脚本
    """
    drop()
    t = time.time()
    sys.stdout.write('start hx crawl...\n')
    jobs = map(lambda x: gevent.spawn(profile, CRAWL_URLS['HX'] % x, {}), range(1, 1339))
    gevent.joinall(jobs)
    global data
    jobs = map(lambda x: gevent.spawn(text, x, data[x][0], {}), range(1, len(data)))
    gevent.joinall(jobs)
    t1 = time.time() - t
    sys.stdout.write('done hx crawl cost %.3f s\n' % t1)

    data = filter(lambda x: len(x) == 7, data)

    sys.stdout.write('total: %s\n' % len(data))

    t = time.time()
    sys.stdout.write('start hx MySQLdb executemany...\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='britten', db='wemedia_crawl', charset='utf8')
    cursor = conn.cursor()
    sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, data)
    conn.commit()
    conn.close()
    t2 = time.time() - t
    sys.stdout.write('done hx MySQLdb executemany cost %.3f s\n' % t2)
    return t1, t2


if __name__ == '__main__':
    run()
