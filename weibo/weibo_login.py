# -*- coding: utf-8 -*-
# @Time        : 2019/9/18 10:51
# @Author      : tianyunzqs
# @Description : 

import time
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='../phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.get('https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F')
print(driver.page_source)
time.sleep(2)

weiboUrl = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'
user = 'tianyunzqs@sina.com'
password = 'tianyun618'
driver.get(weiboUrl)
time.sleep(5)
driver.find_element_by_id('loginName').clear()
driver.find_element_by_id('loginName').send_keys(user)
driver.find_element_by_id('loginPassword').clear()
driver.find_element_by_id('loginPassword').send_keys(password)
driver.find_element_by_id('loginAction').click()
print("logined")
print(driver.page_source)
