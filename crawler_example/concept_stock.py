# -*- coding: utf-8 -*-
# @Time        : 2022/3/30 18:01
# @Author      : tianyunzqs
# @Description :

import re
import time
import json
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from free_proxy_ip_pool import ProxyFactory
from free_proxy_ip_pool.agent import useragent

factory = ProxyFactory()
headers = {
    'user-agent': useragent.chrome
}


def sleep_random(start=1, end=1.5):
    time.sleep(random.randrange(int(start * 100), int(end * 100), step=1) * 0.01)


def get_all_concept_link_page_source():
    link_name = dict()
    with open('dd.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            link, name = line.strip().split('\t')
            new_link = link.replace('conceptDetail', 'conceptStock').replace('shtml', 'js')
            link_name[new_link] = name
    # try:
    #     # www = factory.create('https://www.kuaidaili.com/free', headers=headers)
    #     www = factory.create('http://www.ip3366.net/', 'gbk', headers=headers)
    #     # www = factory.create('http://www.goubanjia.com/',headers = headers)
    #     # www = factory.create('http://www.data5u.com/', headers=headers)
    #     # www = factory.create('http://www.89ip.cn/', headers=headers)
    #     # www = factory.create('https://ip.ihuan.me/', headers=headers)
    #     # www = factory.create(
    #     #     'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=',
    #     #     'gbk',
    #     #     headers=headers)
    #     data = www.run()
    # except:
    #     return
    for link, name in link_name.items():
        print(name, link)
        with open(name.replace('/', '-') + '.txt', 'w', encoding='utf-8') as f:
            while True:
                try:
                    www = factory.create('http://www.ip3366.net/', 'gbk', headers=headers)
                    data = www.run()
                except:
                    return
                flag = False
                for d in tqdm(data):
                    try:
                        page_source = requests.get(link, timeout=2, headers=headers, proxies={"http": '{0}:{1}'.format(d.host, d.port)})
                        json_str = page_source.content.decode('gbk')
                        json_str = json_str.replace('var conceptstockdata=', '').rstrip(';')
                        result = json.loads(json_str)
                        f.write(json.dumps(result, ensure_ascii=False))
                        sleep_random()
                    except:
                        sleep_random()
                        continue
                    flag = True
                    break
                if flag:
                    break


def get_alive_ip(test_url):
    alive_ip_list = []
    www = factory.create('https://www.kuaidaili.com/free', headers=headers)
    data = www.run()
    for d in tqdm(data):
        try:
            respond = requests.get(test_url,
                                   proxies={"http": '{0}:{1}'.format(d.host, d.port)},
                                   timeout=2)
            if respond.status_code == 404:
                continue
            alive_ip_list.append("{0}:{1}".format(d.host, d.port))
        except:
            continue
    return alive_ip_list


if __name__ == '__main__':
    # url = 'http://stock.jrj.com.cn/concept/conceptpage.shtml?to=pc'
    # a = get_alive_ip(url)
    # print(a)
    get_all_concept_link_page_source()
