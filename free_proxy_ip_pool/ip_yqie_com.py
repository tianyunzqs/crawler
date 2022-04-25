from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
免费代理IP http://ip.yqie.com/ipproxy.htm
'''


class IP_YQIE_COM(AbsFreeProxyBase):

    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        采集到的数据格式如下
        '183.148.153.200', '9999', '浙江台州', '高匿', 'HTTPS', '1分钟'
        """
        regex = re.compile( r'(?<=<td>)(.*)(?=</td>)')
        container = soup.select('.divcenter tr')
        result = []
        for text in [str(n) for n in container]:
            item = regex.findall(text)
            item and result.append(item)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            result.append(ProxyModel(item[4], item[0], item[1], item[3]))
        return result
