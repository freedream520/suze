# -*- coding: utf-8 -*-

import urllib
import time

from requests import get


def retrieve(url, params):
    """
    下载页面
    """
    _url = url ,urllib.urlencode(params)
    print 'retrieve...', _url, time.strftime('%H:%M:%S')
    content = get(url, params=params, timeout=30).content
    print 'retrieve done', _url, time.strftime('%H:%M:%S')
    return content
