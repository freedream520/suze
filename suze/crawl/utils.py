# -*- coding: utf-8 -*-

import urllib
import time
import sys

from requests import get


def retrieve(url, params):
    """
    下载页面
    """
    _url = url ,urllib.urlencode(params)
    sys.stdout.write('retrieve... %s %s\n' % (_url, time.strftime('%H:%M:%S')))
    content = get(url, params=params, timeout=30).content
    sys.stdout.write('retrieve done %s %s\n' % (_url, time.strftime('%H:%M:%S')))
    return content
