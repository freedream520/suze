# -*- coding: utf-8 -*-

"""
36氪爬虫脚本
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
    t = tree.xpath("//section[@class='article']/*")
    _content = ''.join(map(lambda x: etree.tostring(x, encoding='utf-8'), t))
    data[i].append(_content)


def profile(url, params):
    """
    抓取保存封面，标题，摘要
    """
    content = retrieve(url, params)
    tree = etree.HTML(content)

    for x in tree.xpath("//article[@class='posts post-1 cf']"):
        cover = x.find("div[@class='left left-col']/div[2]/a/img").attrib['data-src']
        title = x.find("div[@class='right-col']/h1/a").text
        url = 'http://www.36kr.com' + x.find("div[@class='right-col']/h1/a").attrib['href']
        brief = x.find("div[@class='right-col']/p").text
        author = '36氪'
        code = '36kr'

        data.append([url, cover, title, brief, author, code])


def drop():
    sql = 'DELETE FROM article WHERE code=%s'
    DB.update(sql, '36kr')


def run():
    """
    启动脚本
    """
    drop()
    t = time.time()
    sys.stdout.write('start 36kr crawl...\n')
    jobs = map(lambda x: gevent.spawn(profile, CRAWL_URLS['KR'], {'page':x}), range(1, 101))
    gevent.joinall(jobs)
    global data
    jobs = map(lambda x: gevent.spawn(text, x, data[x][0], {}), range(1, len(data)))
    gevent.joinall(jobs)
    t1 = time.time() - t
    sys.stdout.write('done 36kr crawl cost %.3f s\n' % t1)


    data = filter(lambda x: len(x) == 7, data)

    total = len(data)
    sys.stdout.write('total: %s\n' % total)

    t = time.time()
    sys.stdout.write('start 36kr MySQLdb executemany...\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='britten', db='wemedia_crawl', charset='utf8')
    cursor = conn.cursor()
    sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, data)
    conn.commit()
    conn.close()
    t2 = time.time() - t
    sys.stdout.write('done 36kr MySQLdb executemany cost %.3f s\n' % t2)
    return t1, t2, 101, total


if __name__ == '__main__':
    run()
