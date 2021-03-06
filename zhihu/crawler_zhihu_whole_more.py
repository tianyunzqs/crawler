#!usr/bin/env python
# -*- coding: utf-8 -*-

import time
import re
from urllib import request, parse
from bs4 import BeautifulSoup
from selenium import webdriver


def get_grade(url):
    # 匿名爬虫
    driver = webdriver.PhantomJS(executable_path='E:/phantomjs/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url)
    data = driver.page_source
    return data, driver


# keyword_list = ['svm', '支持向量机', 'libsvm']
# keyword_list = ['java']
keyword_list = ['核函数', 'kernel', '径向基函数', 'sigmoid', 'tanh', 'rbf']
fout = open("E:/python_file/kernel.txt", "w", encoding="utf-8")
for keyword in keyword_list:
    print(keyword)
    # 将中文转换为浏览器可识别字符（HTTP协议是ASCII编码的形式）
    url = 'https://www.zhihu.com/search?type=content&q=' + parse.quote(keyword)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/39.0.2171.95 Safari/537.36'
    headers = {'User-Agent': user_agent}
    keyword_question_url_list = {}
    try:
        content, driver = get_grade(url)

        cnt = 0
        while True:
            try:
                cnt += 1
                print(cnt)
                if cnt > 6:
                    break
                aaa = driver.find_element_by_css_selector('.zg-btn-white.zu-button-more')
            except:
                break
            time.sleep(10)
            aaa.click()
            time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
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
    except:
        continue

    for keyword, question_url_list in keyword_question_url_list.items():
        for question, url in question_url_list.items():
            fout.write(question + "\n")
            try:
                req = request.Request(url, headers=headers)
                content, driver = get_grade(url)
                soup = BeautifulSoup(content, 'html.parser')
                if re.search('https://zhuanlan.zhihu.com/p/[0-9]+', url):
                    answer = soup.find_all('div', attrs={'class': 'RichText PostIndex-content av-paddingSide av-card'})
                    answer = answer[0].text
                    fout.write(answer + "\n")
                elif re.search('https://www.zhihu.com/question/[0-9]+', url):
                    all_div = soup.find_all('div', attrs={'class': 'List-item'})
                    print(len(all_div))
                    for e_div in all_div:
                        answer = e_div.find_all('span', attrs={'class': 'RichText CopyrightRichText-richText',
                                                               'itemprop': 'text'})
                        answer = answer[0].text
                        fout.write(answer + "\n")
                else:
                    continue
            except:
                continue
