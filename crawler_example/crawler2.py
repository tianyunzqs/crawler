#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import request
from bs4 import BeautifulSoup


def find_all(item, attr, c):
    return item.find_all(attr, attrs={'class': c}, limit=1)

for page in range(1, 20):
    print(page)
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            all_div = soup.find_all('div', attrs={'class': re.compile('article block untagged mb15 .*?')})
            for i, e_div in enumerate(all_div):
                result = {}
                result['id'] = e_div.attrs['id']
                result['name'] = e_div.h2.string.strip()
                cont = e_div.find_all('div', attrs={'class': 'content'})
                result['content'] = cont[0].text.strip()
                silme_comment = e_div.find_all('i', attrs={'class': 'number'})
                result['silme_num'] = int(silme_comment[0].text.strip())
                result['comment_num'] = int(silme_comment[1].text.strip())
                print(result)
    except request.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
