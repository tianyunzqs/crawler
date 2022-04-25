from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
小幻HTTP代理 https://ip.ihuan.me/
'''


class IP_IHUAN_ME(AbsFreeProxyBase):
   
    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式：
        IP地址	端口	地理位置	运营商	HTTPS(支持/不支持)	POST(支持/不支持)	匿名度	访问速度	入库时间	最后检测
        """
        rows = soup.select('.table-bordered tr')
        result = []
        for row in rows:
            cols = row.select('td')
            item = [re.sub(r'\s', "", c.get_text()) for c in cols]
            item and result.append(item)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            scheme = 'http and https' if item[4] == '支持' else 'http'
            result.append(ProxyModel(scheme, item[0], item[1], item[6]))
        return result