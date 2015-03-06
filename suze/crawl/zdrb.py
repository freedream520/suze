# -*- coding: utf-8 -*-

"""
百度知道日报爬虫脚本
"""

import gevent
import gevent.monkey
gevent.monkey.patch_socket()
import time
import sys
import MySQLdb

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
    t = tree.xpath("//div[@id='daily-cont']/*")
    _content = ''.join(map(lambda x: etree.tostring(x, encoding='utf-8'), t))
    data[i].append(_content)


def profile(url, params):
    """
    抓取保存封面，标题，摘要
    """
    content = retrieve(url, params)
    tree = etree.HTML(content)

    for x in tree.xpath("//ul[@class='daily-list']/li"):
        cover = x.find('a/img').attrib['src']
        title = x.find("div[@class='daily-cont']/h2/a").text
        url = 'http://zhidao.baidu.com' + x.find("div[@class='daily-cont']/h2/a").attrib['href']
        brief = x.find("div[@class='daily-cont']/div[@class='summer']/a").text
        author = '知道日报'
        code = 'zdrb'

        data.append([url, cover, title, brief, author, code])


def drop():
    sql = 'DELETE FROM article WHERE code=%s'
    DB.update(sql, 'zdrb')


def run():
    """
    启动脚本
    """
    drop()
    t = time.time()
    sys.stdout.write('start zdrb crawl...\n')
    jobs = map(lambda x: gevent.spawn(profile, CRAWL_URLS['ZDRB'], {'period':x}), range(1, 553))
    gevent.joinall(jobs)
    global data
    jobs = map(lambda x: gevent.spawn(text, x, data[x][0], {}), range(1, len(data)))
    gevent.joinall(jobs)
    t1 = time.time() - t
    sys.stdout.write('done zdrb crawl cost %.3f s\n' % t1)

    data = filter(lambda x: len(x) == 7, data)

    sys.stdout.write('total: %s\n' % len(data))

    t = time.time()
    sys.stdout.write('start zdrb MySQLdb executemany...\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='britten', db='wemedia_crawl', charset='utf8')
    cursor = conn.cursor()
    sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, data)
    conn.commit()
    conn.close()
    t2 = time.time() - t
    sys.stdout.write('done zdrb MySQLdb executemany cost %.3f s\n' % t2)
    return t1, t2


if __name__ == '__main__':
    run()
