from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
http://www.goubanjia.com/
全网代理IP 
'''


class WWW_GOUBANJIA_COM(AbsFreeProxyBase):

    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式
        IP:PORT 	匿名度 	类型 	IP归属地 	运营商 	响应速度 	最后验证时间 	存活时间
        """
        rows = soup.select('.table-hover tr')
        result = []
        for r in rows:
            for p in r.find_all('p'):
                p.extract()
            cols = [re.sub(r'\s', "", c.get_text()) for c in r.select('td')]
            cols and result.append(cols)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            host, port = re.search(r'([\d.]+):(\d+)', item[0]).groups()
            result.append(ProxyModel(item[2], host, port, item[1]))
        return result
