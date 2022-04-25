from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
https://www.zdaye.com/dayProxy/ip/316788.html
'''
class WWW_ZDAYE_COM(AbsFreeProxyBase):
   
    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式：
        IP，端口，协议，匿名度
        """
        regex = re.compile(
            r'([\d.]+):(\d+)@(HTTPS?)#\[([\u4e00-\u9fa5]+)\]', re.I)
        text = soup.select('.cont')
        rows = regex.findall(str(text))
        result = []
        for item in rows:
            item and result.append(item)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for host, port, scheme, anonymity in data:
            result.append(ProxyModel(scheme, host, port, anonymity))
        return result
