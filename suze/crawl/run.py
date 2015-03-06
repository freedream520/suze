# -*- coding: utf-8 -*-

"""
启动爬虫脚本
"""

import zdrb
import hx
import kr


if __name__ == '__main__':
    z = zdrb.run()
    h = hx.run()
    k = kr.run()
    print 'zdrb', z
    print 'hx', h
    print 'kr', k
