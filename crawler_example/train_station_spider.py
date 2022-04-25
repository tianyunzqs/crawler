# -*- coding: utf-8 -*-
# @Time        : 2021/9/9 22:17
# @Author      : tianyunzqs
# @Description ：

import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def load_train_stations(path):
    all_station_name, done_province, done_city = [], [], []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = re.sub(r'\\x1e', '', line).strip()
            line = json.loads(line)
            all_station_name.append(line['station_name'])
            if line['province'] not in done_province:
                done_province.append(line['province'])
            if line['city'] not in done_city:
                done_city.append(line['city'])
    return all_station_name, done_province[:-1], done_city[:-1]


standard_key_name = {
    '中文名': 'chinese_name',
    '改建时间': 'build_time',
    '外文名': 'foreign_name',
    '隶属': 'belong',
    '地址': 'address',
    '邮编': 'postcode',
}


def get_alive_ip(test_url):
    cnt, max_retries_count = 0, 50
    while True:
        try:
            ip_info = json.loads(requests.get('https://ip.jiangxianli.com/api/proxy_ip').text)['data']
            respond = requests.get(test_url,
                                   proxies={"http": '{0}:{1}'.format(ip_info['ip'], ip_info['port'])},
                                   timeout=2)
            if respond.status_code == 404:
                return False, ip_info
            cnt += 1
            print('请求 {0} 次 获得可用ip：{1}:{2}'.format(cnt, ip_info['ip'], ip_info['port']))
            return True, ip_info
        except:
            if cnt > max_retries_count:
                raise Exception('Max retries exceeded')

# alive_ip = [
#     '196.10.68.2:80', '222.74.202.230:8080', '222.74.202.234:8081', '51.91.157.66:80', '64.124.38.141:8080',
#     '108.61.26.164:8080', '206.189.89.122:3128', '222.249.238.138:8080', '183.47.237.251:80',
#     '209.141.56.127:80', '153.122.72.63:80'
# ]
# alive_ip = [
#     '197.253.7.201:80', '45.152.188.39:3128', '121.78.139.77:80', '136.243.211.104:80', '52.20.205.11:80'
# ]


all_station_names, done_provinces, done_cities = load_train_stations('train_stations.txt')
print(all_station_names)
print(done_provinces)
print(done_cities)


_, ip_port = get_alive_ip('http://huochezhan.114piaowu.com')
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument(('--proxy-server=http://{0}:{1}'.format(ip_port['ip'], ip_port['port'])))

chrome_options2 = Options()
chrome_options2.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
chrome_options2.add_argument('--disable-dev-shm-usage')
chrome_options2.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
chrome_options2.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options2.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options2.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options2.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options2.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options2.add_argument(('--proxy-server=http://{0}:{1}'.format(ip_port['ip'], ip_port['port'])))

chrome_options3 = Options()
chrome_options3.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
chrome_options3.add_argument('--disable-dev-shm-usage')
chrome_options3.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
chrome_options3.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options3.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options3.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options3.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options3.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options3.add_argument(('--proxy-server=http://{0}:{1}'.format(ip_port['ip'], ip_port['port'])))

browser = webdriver.Chrome(chrome_options=chrome_options)
browser2 = webdriver.Chrome(chrome_options=chrome_options2)
browser3 = webdriver.Chrome(chrome_options=chrome_options3)

while True:
    try:
        browser.get('http://huochezhan.114piaowu.com')
        all_province_stations = browser.find_element_by_id('content').find_elements_by_tag_name('dd')
        break
    except:
        _, ip_port = get_alive_ip('http://huochezhan.114piaowu.com')
        chrome_options.add_argument(('--proxy-server=http://{0}:{1}'.format(ip_port['ip'], ip_port['port'])))
        browser = webdriver.Chrome(chrome_options=chrome_options)
        print('browser---{0}:{1}'.format(ip_port['ip'], ip_port['port']))

with open('train_stations.txt', 'a', encoding='utf-8') as f:
    for province in all_province_stations:
        province_name = province.find_element_by_tag_name("font").text
        if province_name in done_provinces:
            continue
        print('province_name: ', province_name)
        all_city_stations = province.find_elements_by_tag_name("span")
        for city in all_city_stations:
            city_sites = city.find_elements_by_tag_name("a")
            for city_site in city_sites:
                city_name = city_site.text
                if city_name in done_cities:
                    continue
                print('city_name: ', city_name)
                href = city_site.get_attribute("href")
                time.sleep(0.1)

                city_flag = True
                while True:
                    try:
                        browser2.get(href)
                        stations_elems = browser2.find_element_by_class_name("train_list").find_element_by_tag_name(
                            "ul").find_elements_by_tag_name("li")
                        break
                    except:
                        city_flag, ip_port = get_alive_ip(href)
                        if not city_flag:
                            break
                        chrome_options2.add_argument(('--proxy-server=http://{0}:{1}'.format(
                            ip_port['ip'], ip_port['port'])))
                        browser2 = webdriver.Chrome(chrome_options=chrome_options2)
                        print('browser2---{0}:{1}'.format(ip_port['ip'], ip_port['port']))
                if not city_flag:
                    continue

                for st in stations_elems:
                    station_name = st.find_element_by_tag_name("dt").find_element_by_tag_name("a").text
                    if station_name in all_station_names:
                        continue
                    station_href = st.find_element_by_tag_name("dt").find_element_by_tag_name("a").get_attribute('href')
                    is_valid_ticket = st.find_element_by_tag_name("dd").find_elements_by_tag_name("p")[0].text
                    if re.search('未开通', is_valid_ticket):
                        is_valid_ticket = 0
                    else:
                        is_valid_ticket = 1
                    time.sleep(0.1)

                    station_flag = True
                    while True:
                        try:
                            browser3.get(station_href + '_introduce')
                            about = browser3.find_element_by_class_name('about')
                            break
                        except:
                            station_flag, ip_port = get_alive_ip(station_href + '_introduce')
                            if not station_flag:
                                break
                            chrome_options3.add_argument(('--proxy-server=http://{0}:{1}'.format(
                                ip_port['ip'], ip_port['port'])))
                            browser3 = webdriver.Chrome(chrome_options=chrome_options3)
                            print('browser3---{0}:{1}'.format(ip_port['ip'], ip_port['port']))
                    if not station_flag:
                        continue

                    pic_url = about.find_element_by_tag_name('img').get_attribute('src')
                    try:
                        introduce = about.find_element_by_tag_name('p').text
                    except:
                        introduce = about.text
                        introduce = re.sub(r'^[\s\S]{0,15}介绍[。,，]?', '', introduce)
                        introduce = re.sub('中文名\n[\s\S]*$', '', introduce).strip()
                        introduce = re.sub('暂无', '', introduce).strip()
                    attrs = about.find_element_by_tag_name('ul').find_elements_by_tag_name('li')
                    attrs_json = dict()
                    for attr in attrs:
                        key = attr.find_element_by_tag_name('span').text.strip()
                        value = re.sub(r'^{0}\s*'.format(key), '', attr.text).strip()
                        if key in standard_key_name:
                            attrs_json[standard_key_name[key]] = value

                    station_info = {
                        'province': province_name,
                        'city': city_name,
                        'station_name': station_name,
                        'pic_url': pic_url,
                        'is_valid_ticket': is_valid_ticket,
                        'introduce': introduce,
                    }
                    station_info.update(attrs_json)
                    print(station_info)
                    f.write(json.dumps(station_info, ensure_ascii=False))
                    f.write('\n')
                    f.flush()
                    # result.append(station_info)

# data = pd.DataFrame(result)
# data.to_csv('train_stations.csv', index=False)
