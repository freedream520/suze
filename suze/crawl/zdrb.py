# -*- coding: utf-8 -*-

"""
百度知道日报爬虫脚本

cover, title, brief, content, content_html, author=知道日报
"""

import gevent
import gevent.monkey
gevent.monkey.patch_socket()
import time
import pickle

from lxml import etree
from db import DB
from settings import CRAWL_URLS
from utils import retrieve

data = [None]

def insert():
    sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    return DB.insertmany(sql, data)


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
    print 'start zdrb crawl...'
    jobs = map(lambda x: gevent.spawn(profile, CRAWL_URLS['ZDRB'], {'period':x}), range(1, 553))
    gevent.joinall(jobs)
    global data
    _data = [None]
    _data.extend(filter(len, data[1:]))
    data = _data
    jobs = map(lambda x: gevent.spawn(text, x, data[x][0], {}), range(1, len(data)))
    gevent.joinall(jobs)
    print 'done zdrb crawl cost %.3f s' % (time.time() - t)

    data = data[1:]
    data = filter(lambda x: len(x) == 7, data)
    print len(data)

    with open('data', 'wb') as f:
        pickle.dump(data, f)

    # with open('data', 'rb') as f:
        # data = pickle.load(f)

    # data = filter(lambda x: len(x) == 7, data)
    # print len(data)
    # t = time.time()
    # print 'start zdrb MySQLdb executemany...'
    # import MySQLdb
    # conn = MySQLdb.connect(host='localhost', user='root', passwd='britten', db='wemedia_crawl', charset='utf8')
    # cursor = conn.cursor()
    # sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    # cursor.executemany(sql, data)
    # conn.commit()
    # print 'done zdrb MySQLdb executemany cost %.3f s' % (time.time() - t)


    # t = time.time()
    # print 'start zdrb insertmany...'
    # insert()
    # print 'done zdrb insertmany cost %.3f s' % (time.time() - t)


if __name__ == '__main__':
    run()
