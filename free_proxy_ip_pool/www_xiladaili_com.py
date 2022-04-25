from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re

'''
http://www.xiladaili.com/http/
http://www.xiladaili.com/gaoni/
'''


class WWW_XILADAILI_COM(AbsFreeProxyBase):
  
    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式
        代理IP(xxx.xxx.xxx:port) 	代理协议 	IP匿名度 	代理位置 	响应速度 	存活时间 	最后验证时间 	打分
        """
        regex = re.compile(r'(?<=<td>)(.*)(?=</td>)')
        rows = soup.select('.fl-table tr')
        result = []
        for row in [str(n) for n in rows]:
            item = regex.findall(row)
            item and result.append(item)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            host, port = re.search(r'([\d.]+):(\d+)', item[0]).groups()
            result.append(ProxyModel(item[1], host, port, item[2]))
        return result