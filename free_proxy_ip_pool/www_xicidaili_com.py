from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
https://www.xicidaili.com/wt/ 代理

'''


class WWW_XICIDAILI_COM(AbsFreeProxyBase):

     # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式如下：
        "ip", "端口", "协议", "存活时间", "验证时间"
        """
        regex = re.compile(r'(?<=<td>)(.*)(?=</td>)')
        rows = soup.select('#ip_list tr')
        result = []
        for row in [str(n) for n in rows]:
            item = regex.findall(row)
            item and result.append(item)
        return result

        # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            result.append(ProxyModel(item[2], item[0], item[1]))
        return result
