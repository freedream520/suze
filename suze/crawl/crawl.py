# -*- coding: utf-8 -*-

"""
爬虫脚本

数据来源: 知道日报、虎嗅、36氪
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


class Crawl:
    def __init__(self, start_url, site_name):
        self.data = [[]]
        self.start_url = start_url
        self.site_name = site_name

    def gen_profiles(self):
        raise NotImplementedError

    def gen_texts(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def run(self):
        self.drop()

        # 抓取数据到内存
        t = time.time()
        sys.stdout.write('start %s crawl...\n' % self.site_name)
        gevent.joinall(self.gen_profiles())
        gevent.joinall(self.gen_texts())
        sys.stdout.write('done %s crawl cost %.3f s\n' % (self.site_name, time.time() - t))
        self.data = filter(lambda x: len(x) == 7, self.data)
        sys.stdout.write('total: %s\n' % len(self.data))

        # 持久化到数据库
        t = time.time()
        sys.stdout.write('start %s executemany...\n' % self.site_name)
        conn = MySQLdb.connect(host='localhost', user='root', passwd='britten', db='wemedia_crawl', charset='utf8')
        cursor = conn.cursor()
        sql = 'INSERT INTO article(url, cover, title, brief, author, code, content) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.executemany(sql, self.data)
        conn.commit()
        conn.close()
        sys.stdout.write('done %s executemany cost %.3f s' % (self.site_name, time.time() - t))


class ZDRBCrawl(Crawl):
    def __init__(self):
        Crawl.__init__(self, CRAWL_URLS['ZDRB'], 'zdrb')

    def profile(self, url, params):
        tree = etree.HTML(retrieve(url, params))

        for x in tree.xpath("//ul[@class='daily-list']/li"):
            cover = x.find('a/img').attrib['src']
            title = x.find("div[@class='daily-cont']/h2/a").text
            url = 'http://zhidao.baidu.com' + x.find("div[@class='daily-cont']/h2/a").attrib['href']
            brief = x.find("div[@class='daily-cont']/div[@class='summer']/a").text
            author = '知道日报'
            code = 'zdrb'

            self.data.append([url, cover, title, brief, author, code])

    def text(self, i, url, params):
        content = retrieve(url, params)
        tree = etree.HTML(content)
        t = tree.xpath("//div[@id='daily-cont']/*")
        _content = ''.join(map(lambda x: etree.tostring(x, encoding='utf-8'), t))
        self.data[i].append(_content)

    def drop(self):
        sql = 'DELETE FROM article WHERE code=%s'
        DB.update(sql, 'zdrb')

    def gen_profiles(self):
        return map(lambda x: gevent.spawn(self.profile, CRAWL_URLS['ZDRB'], {'period':x}), range(1, 553))

    def gen_texts(self):
        return map(lambda x: gevent.spawn(self.text, x, self.data[x][0], {}), range(1, len(self.data)))


if __name__ == '__main__':
    crawls = [ZDRBCrawl()]
    jobs = map(lambda x: gevent.spawn(x.run), crawls)
    gevent.joinall(jobs)
