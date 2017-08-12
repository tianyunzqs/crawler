#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import request
from bs4 import BeautifulSoup

url = 'https://www.zhihu.com/question/20981010'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/39.0.2171.95 Safari/537.36'
headers = {'User-Agent': user_agent}

try:
    req = request.Request(url, headers=headers)
    with request.urlopen(req, timeout=10) as response:
        content = response.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        all_div = soup.find_all('div', attrs={'class': 'List-item'})
        for e_div in all_div:

            answer = e_div.find_all('span', attrs={'class': 'RichText CopyrightRichText-richText', 'itemprop': 'text'})
            print(answer[0].text)
            break

except request.URLError as e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)
