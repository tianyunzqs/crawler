from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
无忧代理 http://www.data5u.com/

'''


class WWW_DATA5U_COM(AbsFreeProxyBase):

    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)


    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式如下
        IP、端口、匿名度、类型(http/https)、国家、省市、运营商、响应速度、最后验证时间
        [
           [...]
           [...]
        ]
        """
        rows = soup.select('.l2')
        result = []
        for row in rows:
            col = [n.string.strip() for n in row.find_all('li')]
            col and result.append(col)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            result.append(ProxyModel(item[4], item[0], item[1], item[2]))
        return result