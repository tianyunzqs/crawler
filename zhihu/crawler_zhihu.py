#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib import request
from bs4 import BeautifulSoup

keyword_list = ['svm', '支持向量机', 'libsvm', '']
fout = open("E:/python_file/zhihu.txt", "w", encoding="utf-8")
for keyword in keyword_list:
    print(keyword)
    url = 'https://www.zhihu.com/search?type=content&q=' + str(keyword)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/39.0.2171.95 Safari/537.36'
    headers = {'User-Agent': user_agent}
    keyword_question_url_list = {}
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req, timeout=5)
        content = response.read().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        all_div = soup.find_all('li', attrs={'class': re.compile('item clearfix.*?')})
        question_url_list = {}
        for e_div in all_div:
            title = e_div.find_all('a', attrs={'class': 'js-title-link',
                                               'target': '_blank',
                                               'href': re.compile('/question/[0-9]+')})
            if title:
                title = title[0].text
                _id = e_div.find_all('link', attrs={'itemprop': 'url',
                                                    'href': re.compile('/question/[0-9]+/answer/[0-9]+')})
                href = _id[0].attrs.get('href')
                pattern = re.compile('/question/(.*?)/answer/(.*?)$', re.S)
                items = re.findall(pattern, href)
                question_id = items[0][0]
                question_url_list[title] = 'https://www.zhihu.com/question/' + question_id
            else:
                title_id = e_div.find_all('a', attrs={'class': 'js-title-link',
                                                   'target': '_blank',
                                                   'href': re.compile('https://zhuanlan.zhihu.com/p/[0-9]+')})
                if title_id:
                    title = title_id[0].text
                    href = title_id[0].attrs.get('href')
                    question_url_list[title] = href
                else:
                    continue
        keyword_question_url_list[keyword] = question_url_list
        # for q, d in question_url_list.items():
        #     print(q, d)
    except:
        continue

    for keyword, question_url_list in keyword_question_url_list.items():
        for question, url in question_url_list.items():
            fout.write(question + "\n")
            try:
                req = request.Request(url, headers=headers)
                with request.urlopen(req, timeout=5) as response:
                    content = response.read().decode('utf-8')
                    soup = BeautifulSoup(content, 'html.parser')
                    all_div = soup.find_all('div', attrs={'class': 'List-item'})
                    for e_div in all_div:
                        answer = e_div.find_all('span', attrs={'class': 'RichText CopyrightRichText-richText',
                                                               'itemprop': 'text'})
                        answer = answer[0].text
                        fout.write(answer + "\n")
            except request.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)