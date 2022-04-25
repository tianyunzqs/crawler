from .base import AbsFreeProxyBase
from typing import List
from .model import ProxyModel
import re
'''
www.89ip.cn 免费代理爬取
'''


class WWW_89IP_CN(AbsFreeProxyBase):

    '''
    初始化
    '''

    # 初始化
    def __init__(self, url, code='utf-8', **kwargs):
        super().__init__(url, code, **kwargs)

    # 解析内容
    def parse_text(self, soup) -> List[list]:
        """
        数据格式如下
        'IP地址', '端口', '地理位置', '运营商', '最后检测'
        [
            ['222.189.190.242', '9999', '江苏省扬州市', '电信', '2019/11/10'], 
            ['58.253.153.206', '9999', '广东省揭阳市', '联通', '2019/11/10'], 
            ['183.164.238.17', '9999', '安徽省淮北市', '电信', '2019/11/10'],
            ...
        ]
        """
        rows = soup.select('.layui-table tr')
        result = []
        for row in rows:
            col = [n.string.strip() for n in row.find_all('td')]
            col and result.append(col)
        return result

    # 格式转换
    def to_proxy(self, data: List[list]) -> List[ProxyModel]:
        result = []
        for item in data:
            result.append(ProxyModel('http', item[0], item[1]))
        return result
