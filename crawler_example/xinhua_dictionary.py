# -*- coding: utf-8 -*-
# @Time        : 2022/4/25 15:52
# @Author      : tianyunzqs
# @Description :

import os
import re
import sys
import time
import random
import datetime
import collections
import requests
from bs4 import BeautifulSoup
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from free_proxy_ip_pool import ProxyFactory
from free_proxy_ip_pool.agent import useragent
from utils.mysql_utils import MysqlClient

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


def get_requests(url, header, one_proxy=None):
    if not one_proxy:
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
    return respond, one_proxy


def load_exist_url():
    mysql_instance = MysqlClient(host='localhost',
                                 user='root',
                                 password='dyty2502',
                                 database='datasets',
                                 port=3306)
    sql = "SELECT url FROM xhzd"
    return set([item['url'] for item in mysql_instance.query(sql)])


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
    exist_urls = load_exist_url()
    main_url = 'http://xh.5156edu.com'
    result = collections.defaultdict(dict)
    pinyin_url = get_pinyin_url('pinyin_url.txt')
    valid_proxy = get_proxy()
    for pinyin, url in pinyin_url.items():
        respond, valid_proxy = get_requests(url, header, valid_proxy)
        page_source = respond.content.decode('gbk', errors='ignore')
        for item in re.finditer(r"class='fontbox' href='(?P<href>.*?)'>(?P<char>.)<", page_source):
            hanzi = item.groupdict()['char']
            char_url = main_url + item.groupdict()['href']
            if char_url in exist_urls:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hanzi, char_url, "跳过")
                continue
            # char_url = main_url + '/html3/1617.html'
            # char_url = main_url + '/html3/7578.html'
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hanzi, char_url)
            result[hanzi] = {
                "url": char_url,
                "拼音": list(),
                "笔画": -1,
                "部首": '',
                "五笔": '',
                "笔顺编号": '',
                "成语": set(),
                "同部首": set(),
                "同笔画": set(),
                "基本解释": '',
                "笔划顺序": '',
                "详细解释": '',
                "相关词语": set(),
            }
            char_respond, valid_proxy = get_requests(char_url, header, valid_proxy)
            char_respond.encoding = char_respond.apparent_encoding
            char_soup = BeautifulSoup(char_respond.content.decode('gbk', errors='ignore'), 'html.parser')
            td_tag = char_soup.findAll('tr')
            i = 0
            pinyin_tongyin_dict = collections.defaultdict(set)
            pinyin_pinyin_dict = dict()
            while i < len(td_tag):
                td_tag_text = td_tag[i].text.strip()
                if '相关成语' == td_tag_text:
                    i += 1
                    if "更多相关成语" in td_tag[i].text.strip():
                        more_cy_url = main_url + td_tag[i].find('p').find('a').get('href')
                        more_cy_respond, valid_proxy = get_requests(more_cy_url, header, valid_proxy)
                        more_cy_soup = BeautifulSoup(more_cy_respond.content.decode('gbk', errors='ignore'),
                                                     'html.parser')
                        for sub_soup in more_cy_soup.findAll(name="td", attrs={"width": "25%"}):
                            result[hanzi]["成语"].add(sub_soup.text.strip())
                    else:
                        for sub_soup in td_tag[i].findAll('a'):
                            result[hanzi]["成语"].add(sub_soup.text.strip())
                elif '同音字' == td_tag_text:
                    i += 1
                    char_pinyin = ''
                    for bb in td_tag[i].findAll():
                        if bb.name == 'span':
                            char_pinyin = bb.text.strip()
                        elif bb.name == 'a':
                            pinyin_tongyin_dict[char_pinyin].add(bb.text.strip())
                elif '同部首' == td_tag_text:
                    i += 1
                    for sub_soup in td_tag[i].findAll('a'):
                        result[hanzi]["同部首"].add(sub_soup.text.strip())
                elif '同笔画' == td_tag_text:
                    i += 1
                    for sub_soup in td_tag[i].findAll('a'):
                        result[hanzi]["同笔画"].add(sub_soup.text.strip())
                elif re.search(r'^拼音[\s\S]+笔划', td_tag_text):
                    j = 0
                    e = td_tag[i].findAll('td')
                    while j < len(e):
                        if e[j].text.strip() == "拼音：":
                            j += 1
                            pinyin_pinyin_dict = dict()
                            for re_pinyin in re.finditer(r'>(?P<p1>[^<>(){}]+?)<(script>xhziplay\("(?P<p2>[a-z1-4]+)"\))?', str(e[j])):
                                p1, p2 = re_pinyin.groupdict()['p1'], re_pinyin.groupdict()['p2']
                                if not p1:
                                    continue
                                p1_list = list(filter(None, [w.strip() for w in p1.split(',')]))
                                if not p1_list:
                                    continue
                                for _p1 in p1_list[:-1]:
                                    pinyin_pinyin_dict[_p1] = _p1
                                if p2:
                                    pinyin_pinyin_dict[p1_list[-1]] = p2
                                else:
                                    pinyin_pinyin_dict[p1_list[-1]] = p1_list[-1]

                            all_pinyin = list(filter(None, [w.strip() for w in e[j].text.split(',')]))
                            if len(all_pinyin) != len(pinyin_pinyin_dict):
                                print("拼音长度不一致", char_url)
                        elif e[j].text.strip() == "笔划：":
                            j += 1
                            result[hanzi]["笔画"] = int(e[j].text.strip())
                        j += 1
                elif re.search(r'^部首[\s\S]+五笔', td_tag_text):
                    j = 0
                    e = td_tag[i].findAll('td')
                    while j < len(e):
                        if e[j].text.strip() == "部首：":
                            j += 1
                            result[hanzi]["部首"] = e[j].text.strip()
                        elif e[j].text.strip() == "五笔：":
                            j += 1
                            result[hanzi]["五笔"] = e[j].text.strip()
                        j += 1
                elif re.search(r'^基本解释', td_tag_text) and not result[hanzi]["相关词语"]:
                    parts = re.split(r'(<b><span class="table4">.*?</font></span></b>：)', str(td_tag[i]))
                    j = 0
                    while j < len(parts):
                        if re.search(r'<b><span class="table4">.*?基本解释.*?</font></span></b>：', parts[j]):
                            result[hanzi]["基本解释"] = "\n".join(parts[j:j+2])
                            j += 1
                        elif re.search(r'<b><span class="table4">.*?笔划顺序.*?</font></span></b>：', parts[j]):
                            j += 1
                            bs_part = BeautifulSoup(parts[j], 'html.parser')
                            result[hanzi]["笔划顺序"] = main_url + bs_part.find('img').get('src')
                        elif re.search(r'<b><span class="table4">.*?详细解释.*?</font></span></b>：', parts[j]):
                            result[hanzi]["详细解释"] = "\n".join(parts[j:j+2])
                            j += 1
                        elif re.search(r'<b><span class="table4">.*?相关词语.*?</font></span></b>：', parts[j]):
                            j += 1
                            bs_part = BeautifulSoup(parts[j], 'html.parser')
                            all_relate_words = set()
                            for bp in bs_part.findAll('a'):
                                if re.search(r"更多有关.的词语", bp.text):
                                    more_words_url = main_url + bp.get('href')
                                    more_words_respond, valid_proxy = get_requests(more_words_url, header, valid_proxy)
                                    more_words_soup = BeautifulSoup(
                                        more_words_respond.content.decode('gbk', errors='ignore'),
                                        'html.parser')
                                    for sub_soup in more_words_soup.findAll(name="td", attrs={"width": "25%"}):
                                        all_relate_words.add(sub_soup.text.strip())
                                else:
                                    all_relate_words.add(bp.text)
                            result[hanzi]["相关词语"] = all_relate_words
                        j += 1

                    re_stroke_number = re.search(r'笔顺编号：(?P<number>[1-9]*)', td_tag_text)
                    if re_stroke_number:
                        result[hanzi]["笔顺编号"] = re_stroke_number.groupdict()['number']
                i += 1

            for p1, p2 in pinyin_pinyin_dict.items():
                result[hanzi]["拼音"].append({
                    "拼音1": p1,
                    "拼音2": p2,
                    "同音字": pinyin_tongyin_dict[p1]
                })

            insert_data = []
            for char, char_info in result.items():
                for char_pinyin in char_info["拼音"]:
                    char_py1 = char_pinyin["拼音1"]
                    char_py2 = char_pinyin["拼音2"]
                    char_tyz = "; ".join(char_pinyin["同音字"])
                    insert_data.append([
                        char, char_info["url"], char_py1, char_py2, char_info["笔画"], char_info["部首"],
                        char_info["五笔"], char_info["笔顺编号"], "; ".join(char_info["成语"]), char_tyz,
                        "; ".join(char_info["同部首"]), "; ".join(char_info["同部首"]), char_info["基本解释"],
                        char_info["笔划顺序"], char_info["详细解释"], "; ".join(char_info["相关词语"])
                    ])

            mysql_instance = MysqlClient(host='localhost',
                                         user='root',
                                         password='dyty2502',
                                         database='datasets',
                                         port=3306)
            insert_sql = """
                INSERT INTO xhzd(hanzi, url, pinyin, pinyin2, bihuashu, pianpangbushou, wubi, bishunbianhao, chengyu, tongyinzi, tongbushou, tongbihua, jibenjieshi, bihuashunxu, xiangxijieshi, xiangguanciyu) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            mysql_instance.insert_many(insert_sql, param=insert_data)
            result = collections.defaultdict(dict)


if __name__ == '__main__':
    spider_run()
