from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re


'''
云代理 http://www.ip3366.net/
'''


class WWW_IP3366_NET(AbsFreeProxyBase):

    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式如下
        代理IP地址 	端口 	匿名度 	类型(HTTPS/HTTP) 	get/post支持 	位置 	响应速度 	最后验证时间
        """
        regex = re.compile(r'(?<=<td>)(.*)(?=</td>)')
        rows = soup.select('#list tr')
        result = []
        for row in [str(n) for n in rows]:
            item = regex.findall(row)
            item and result.append(item)
        return result

     # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            result.append(ProxyModel(item[3], item[0], item[1], item[2]))
        return result
