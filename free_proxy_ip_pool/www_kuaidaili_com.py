from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
快代理
https://www.kuaidaili.com/free
'''


class WWW_KUAIDAILI_COM(AbsFreeProxyBase):

    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        格式如下：
        IP 	port(端口) 	匿名度 	类型(HTTP/https) 	位置 	响应速度 	最后验证时间
        """
        regex = re.compile(r'<td[^>]*>([^<>]+)</td>')
        rows = soup.select('.table-bordered tr')
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