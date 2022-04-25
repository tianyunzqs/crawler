class ProxyModel:
    def __init__(self, scheme: str, host: int, port: int, anonymity: str = None):
        """
        格式
        Arguments:
            scheme {str} -- 协议
            host {int} -- 地址
            port {int} -- 端口
            anonymity {str} -- 匿名度
        """
        self.scheme = scheme
        self.host = host
        self.port = port
        self.anonymity = anonymity

    # 获取IP地址
    @property
    def add(self) -> str:
        pass

    # 国籍
    @property
    def country(self) -> str:
        pass

    # 地区
    def city(self) -> str:
        pass

    # 运营商
    def isp(self) -> str:
        pass

    # 验证有效性
    def check(self):
        pass