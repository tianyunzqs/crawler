# -*- coding: utf-8 -*-
# @Time        : 2022/3/10 10:47
# @Author      : tianyunzqs
# @Description :

import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(chrome_options=chrome_options)


def download_video(page_url):
    import requests
    import re
    import json
    import base64

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
    headers = {
        "User-Agent": user_agent
    }
    page_content = requests.get(page_url, headers=headers).content.decode(encoding='utf-8')
    # print(page_content)

    config_info = re.findall(r'window\.__pageState=.*\}</script>', page_content)[0]
    config_info = json.loads(config_info.split('window.__pageState=')[1].replace('</script>', ''))['video']

    title = config_info['title']

    v_sdk = 'https://vas.snssdk.com/video/openapi/v1/'
    params = {
        'action': 'GetPlayInfo',
        'video_id': config_info['vid'],
        'nobase64': 'false',
        'ptoken': config_info['businessToken'],
        'vfrom': 'xgplayer'
    }
    v_header = {
        'Authorization': config_info['authToken'],
        "User-Agent": user_agent
    }
    video_info = json.loads(requests.get(v_sdk, params=params, headers=v_header).content.decode())
    if video_info['code'] == 0:
        h_video = video_info['data']['video_list']['video_' + str(video_info['total'])]
        v_type = h_video['vtype']
        video_url = str(base64.urlsafe_b64decode(h_video['main_url']), encoding='utf-8')
        print(title)
        print(video_url)
        with open('./%s.%s' % (title, v_type), 'wb') as f:
            f.write(requests.get(video_url).content)
        print('下载成功！')
    else:
        print('请求失败!')


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        block_size = 1024  # 1 Kibibyte
        with open(save_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
    else:
        raise Exception("Something went wrong while downloading.")


# # browser.get('https://www.ixigua.com/home/6640492251/video/?preActiveKey=hotsoon&list_entrance=userdetail')
# # browser.get('https://www.ixigua.com/home/6640492251/video')
# browser.get('https://www.ixigua.com/')
# # all_videos = browser.find_elements_by_class_name('HorizontalFeedCard')
# # all_videos = browser.find_elements_by_xpath("//div[@class='HorizontalFeedCard__contentWrapper']")
# all_videos = browser.find_elements_by_xpath("//div[@class='HorizontalFeedCard__contentWrapper']")
# for i, video in enumerate(all_videos):
#     video_url = video.find_element_by_xpath(
#         "//a[@class='HorizontalFeedCard__title color-link-content-primary']").get_attribute('href')
#     download_file(video_url, './{0}.mp4')
download_video('https://www.ixigua.com/7072272558803911199')
