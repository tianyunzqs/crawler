#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import request

for page in range(1, 2):
    print(page)
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            print(content)
            pattern = re.compile(
                '<div class="article block untagged mb15.*?id=(.*?)>.*?<div.*?<a.*?<img.*?<a.*?<h2>(.*?)</h2>'\
                '.*?<a.*?<div.*?<span>(.*?)</span>.*?<!-- 图片或gif -->.*?<div(.*?)<span.*?number">(.*?)</i>'\
                '.*?<i class="number">(.*?)</i>',
                re.S)
            items = re.findall(pattern, content)
            for item in items:
                if not re.search("thumb", item[3]):
                    print(item[0].replace("'", ""), item[1].strip(), item[2].strip(), item[4], item[5])
    except request.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
