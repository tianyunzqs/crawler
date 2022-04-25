# -*- coding: utf-8 -*-
# @Time        : 2021/11/5 17:29
# @Author      : tianyunzqs
# @Description :

import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'''
Function:
    豆瓣模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-10-29
'''
import requests


'''PC端登录豆瓣'''
class doubanPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in douban in pc mode'
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username, password, crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 初始化cookie
        self.session.get(self.home_url)
        # 模拟登录
        data = {
            'ck': '',
            'name': username,
            'password': password,
            'remember': 'true',
            'ticket': ''
        }
        response = self.session.post(self.login_url, data=data)
        response_json = response.json()
        # 登录成功
        if response_json['status'] == 'success':
            print('[INFO]: Account -> %s, login successfully' % username)
            infos_return = {'username': username}
            infos_return.update(response_json)
            return infos_return, self.session
        # 账号或密码错误
        elif response_json['status'] == 'failed' and response_json['message'] == 'unmatch_name_password':
            raise RuntimeError('Account -> %s, fail to login, username or password error' % username)
        # 其他错误
        else:
            raise RuntimeError(response_json.get('description'))
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Host': 'accounts.douban.com',
            'Origin': 'https://accounts.douban.com',
            'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony'
        }
        self.home_url = 'https://www.douban.com/'
        self.login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.session.headers.update(self.headers)


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
data = browser.get('https://www.douban.com/group/707650/discussion?start=50')
print(data)
print(data.content)
