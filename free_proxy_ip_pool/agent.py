import random
import re
from typing import Dict, List
import os


class UserAgent:
    '''
    代理
    '''
    __filepath = 'user-agent.txt'

    '''
    对象实例
    '''
    __instance = None

    '''
    代理浏览器
    '''
    __dict: Dict[str, list] = {}

    '''
    代理浏览器
    '''
    __list: List[str] = []

    '''
    初始化
    '''

    def __init__(self):
        reg = re.compile(r'firefox|chrome|msie|opera', re.I)
        with open(self.filepath, 'r', encoding='utf_8_sig') as f:
            for r in f:
                result = reg.search(r) and reg.search(r).group().lower()
                if result and (not result in self.__dict):
                    self.__dict[result] = []
                result and self.__dict[result].append(r.strip())
                self.__list.append(r.strip())

    @property
    def filepath(self):
        return os.path.join(os.path.dirname(__file__), self.__filepath)

    '''
    单例 - 构造函数
    '''

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(UserAgent, cls).__new__(cls)
        return cls.__instance

    '''
    谷歌
    '''

    @property
    def chrome(self) -> str:
        return random.choice(self.__dict['chrome'])

    '''
    火狐
    '''

    @property
    def firefox(self) -> str:
        return random.choice(self.__dict['firefox'])

    '''
    IE
    '''

    @property
    def ie(self) -> str:
        return random.choice(self.__dict['msie'])

    '''
    Opera 浏览器
    '''

    @property
    def opera(self) -> str:
        return random.choice(self.__dict['opera'])

    '''
    随机
    '''

    def random(self) -> str:
        return random.choice(self.__list)

    '''
    迭代
    '''

    def __iter__(self):
        self.__iter = iter(self.__list)
        return self

    '''
    下一个
    '''

    def __next__(self):
        return next(self.__iter)

    '''
    索引
    '''

    def __getitem__(self, index) -> str or List[str]:
        return self.__list[index]


useragent = UserAgent()
