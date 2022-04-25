from abc import ABC, abstractmethod
from typing import List
import requests
import bs4
from .model import ProxyModel


class AbsFreeProxyBase(ABC):
    # 请求
    http = requests

    # 初始化
    def __init__(self, url, code, **kwargs):
        """
        :param url: 请求地址
        :param code: 页面编码
        :param kw: 附加信息
        """
        self.url = url
        self.code = code
        self.kwargs = kwargs
        self.beautifulsoup = bs4.BeautifulSoup

    # 模板方法模式
    # 第一步 获取页面内容  第二步 解析内容  第二步 格式化数据
    def run(self) -> List[ProxyModel]:
        text = self.get_page_text()
        soup = self.beautifulsoup(text, 'lxml')
        data = self.parse_text(soup)
        return self.to_proxy(data)

    # 获取页面内容
    def get_page_text(self):
        res = AbsFreeProxyBase.http.get(self.url, **self.kwargs)
        if not res.ok:
            res.raise_for_status()
        return res.content.decode(self.code)

    # 解析内容
    @abstractmethod
    def parse_text(self, soup: bs4.BeautifulSoup) -> List[list]:
        pass

    # 格式转换
    @abstractmethod
    def to_proxy(self, data:List[list]) -> List[ProxyModel]:
        pass