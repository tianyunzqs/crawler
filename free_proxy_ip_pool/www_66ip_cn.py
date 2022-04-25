from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
66免费代理网 
http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=
'''


class WWW_66IP_CN(AbsFreeProxyBase):

    # 初始化
    def __init__(self, url, code='gb2312', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
            采集到的数据格式如下
            [
                ('139.199.7.44', '8118'),
                ('212.174.32.244', '80'),
                ('183.129.207.80', '12844')
                ...
            ]
        """
        result, regex = [], re.compile(r'([\d.]+):(\d+)(?=<br\s*/>)')
        for item in regex.findall(str(soup)):
            result.append(item)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for host, port in data:
            result.append(ProxyModel('http', host, port))
        return result
