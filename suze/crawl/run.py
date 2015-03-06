# -*- coding: utf-8 -*-

"""
启动爬虫脚本
"""

import zdrb
import hx
import kr


if __name__ == '__main__':
    t1, t2, v1, v2 = zdrb.run()
    t1, t2, v1, v2 = hx.run()
    t1, t2, v1, v2 = kr.run()
    print 'zdrb', t1, t2, v1, v2
    print 'hx', t1, t2, v1, v2
    print 'kr', t1, t2, v1, v2
