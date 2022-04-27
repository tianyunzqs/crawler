# -*- coding: utf-8 -*-
# @Time        : 2022/4/25 15:52
# @Author      : tianyunzqs
# @Description :

import os
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from free_proxy_ip_pool import ProxyFactory
from free_proxy_ip_pool.agent import useragent
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

factory = ProxyFactory()
headers = {
    'user-agent': useragent.chrome
}
all_www = [
    # 66免费代理网
    factory.create(
        'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
        'gbk',
        headers=headers),
    # 小幻HTTP代理
    factory.create('https://ip.ihuan.me/', headers=headers),
    # 89免费代理
    factory.create('http://www.89ip.cn/', headers=headers),
    # 无忧代理
    factory.create('http://www.data5u.com/', headers=headers),
    # 全网代理IP
    factory.create('http://www.goubanjia.com/', headers=headers),
    # 云代理
    factory.create('http://www.ip3366.net/', 'gbk', headers=headers),
    # 快代理
    factory.create('https://www.kuaidaili.com/free', headers=headers),
]
all_proxy = []


def load_char(path):
    all_chars = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if re.search(r'^[A-Z]$', line):
                continue
            if not line:
                continue
            pinyin, chars = line.split(' ', 1)
            all_chars |= set(chars)
    return all_chars


def get_pinyin_url(path):
    pinyin_url = dict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            url, pinyin = line.split(' ', 1)
            pinyin_url[pinyin] = url
    return pinyin_url


def sleep_random(start=1, end=1.5):
    time.sleep(random.randrange(int(start * 100), int(end * 100), step=1) * 0.01)


def get_proxy():
    if all_proxy:
        return all_proxy.pop()
    else:
        while True:
            try:
                www = all_www[random.randrange(0, len(all_www))]
                data = www.run()
                all_proxy.extend(['{0}:{1}'.format(d.host, d.port) for d in data])
                if all_proxy:
                    return all_proxy.pop()
            except:
                pass


def get_driver():
    one_proxy = get_proxy()
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(('--proxy-server=http://{0}'.format(one_proxy)))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


# def spider_run():
#     pinyin_url = get_pinyin_url('pinyin_url.txt')
#     one_proxy = get_proxy()
#     for pinyin, url in pinyin_url.items():
#         while True:
#             try:
#                 page_source = requests.get(url, timeout=2, headers=headers, proxies={"http": one_proxy})
#
#                 # dcap = DesiredCapabilities.PHANTOMJS.copy()
#                 #
#                 # header = {
#                 #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#                 #     "Accept-Encoding": "gzip, deflate",
#                 #     "Accept-Language": "zh-CN,zh;q=0.9",
#                 #     "Cache-Control": "max-age=0",
#                 #     "Connection": "keep-alive",
#                 #     "Cookie": "__gads=ID=042517c3bb15f02e-225eddf29dcc0050:T=1634605271:RT=1634605271:S=ALNI_MZdY0ASGRC8LZ8ZpG-OPZcDFZERlg; __gpi=UID=00000496cfa1f71c:T=1649322191:RT=1649322191:S=ALNI_MbgHTbNGs2kCXMkYJq1N5zoILN_7w",
#                 #     "Host": "xh.5156edu.com",
#                 #     "Upgrade-Insecure-Requests": "1",
#                 #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
#                 # }
#                 # for key, value in header.items():
#                 #     dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
#                 #
#                 # proxy = [
#                 #     '--proxy=%s' % get_proxy(),  # 设置的代理ip
#                 #     '--proxy-type=http',         # 代理类型
#                 #     '--ignore-ssl-errors=true',  # 忽略https错误
#                 # ]
#                 # driver = webdriver.PhantomJS(
#                 #     executable_path=os.path.join(project_path, 'phantomjs-2.1.1-windows/bin/phantomjs.exe'),
#                 #     desired_capabilities=dcap,
#                 #     service_args=proxy)
#                 # driver.get("http://xh.5156edu.com/pinyi.html")
#                 # print(driver.page_source)
#
#                 # driver.get('http://xh.5156edu.com/')
#                 # a = driver.find_element_by_tag_name('f_key').send_keys(char)
#                 # b = driver.find_element_by_tag_name('SearchString').click()
#             except:
#                 pass
#                 # driver = get_driver()


def get_requests(url, header):
    one_proxy = get_proxy()
    print(one_proxy)
    while True:
        try:
            respond = requests.get(url, timeout=2, headers=header, proxies={"http": one_proxy})
            if respond.status_code == 200 and "Burp Suite Professional" not in respond.text:
                break
            one_proxy = get_proxy()
            print(one_proxy)
            continue
        except:
            one_proxy = get_proxy()
            print(one_proxy)
    return respond


def spider_run():
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "__gads=ID=042517c3bb15f02e-225eddf29dcc0050:T=1634605271:RT=1634605271:S=ALNI_MZdY0ASGRC8LZ8ZpG-OPZcDFZERlg; __gpi=UID=00000496cfa1f71c:T=1649322191:RT=1649322191:S=ALNI_MbgHTbNGs2kCXMkYJq1N5zoILN_7w",
        "Host": "xh.5156edu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    }
    pinyin_url = get_pinyin_url('pinyin_url.txt')
    for pinyin, url in pinyin_url.items():
        respond = get_requests(url, header)
        page_source = respond.content.decode('gbk')
        for item in re.finditer(r"class='fontbox' href='(?P<href>.*?)'>(?P<char>.)<", page_source):
            hanzi = item.groupdict()['char']
            # char_url = 'http://xh.5156edu.com/' + item.groupdict()['href']
            char_url = 'http://xh.5156edu.com/' + 'html3/1617.html'
            # char_url = 'http://xh.5156edu.com/' + 'html3/7578.html'
            char_respond = get_requests(char_url, header)
            char_respond.encoding = char_respond.apparent_encoding
            a = BeautifulSoup(char_respond.content.decode('gbk', errors='ignore'), 'html.parser')
            # b = a.find(name="table", attrs={"id": "table1"})
            # cy = set()
            d = a.findAll('tr')
            i = 0
            # d[i-1].findAll('td')[1].find('script').text
            while i < len(d):
                text = d[i].text.strip()
                if '相关成语' == text:
                    i += 1
                    if "更多相关成语" in d[i].text:
                        more_cy_url = 'http://xh.5156edu.com/' + d[i].find('p').find('a').get('href')
                        more_cy_respond = get_requests(more_cy_url, header)
                        aa = BeautifulSoup(more_cy_respond.content.decode('gbk', errors='ignore'), 'html.parser')
                        for aaa in aa.findAll(name="td", attrs={"width": "25%"}):
                            print(aaa.text.strip())
                    else:
                        for bb in d[i].findAll('a'):
                            print(bb.text.strip())
                elif '同音字' == text:
                    i += 1
                    for bb in d[i].findAll('a'):
                        print(bb.text.strip())
                elif '同部首' == text:
                    i += 1
                    for bb in d[i].findAll('a'):
                        print(bb.text.strip())
                elif '同笔画' == text:
                    i += 1
                    for bb in d[i].findAll('a'):
                        print(bb.text.strip())
                elif re.search(r'拼音[\s\S]+笔划', text):
                    j = 0
                    e = d[i].findAll('td')
                    while j < len(e):
                        if e[j].text.strip() == "拼音：":
                            j += 1
                            print(e[j].find('script').text)
                        elif e[j].text.strip() == "笔划：":
                            j += 1
                            print(e[j].text)
                        j += 1
                    # i += 1
                    for bb in d[i].findAll('td'):
                        print(bb.text.strip())
                i += 1



if __name__ == '__main__':
    spider_run()
