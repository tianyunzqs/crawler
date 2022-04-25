from urllib.parse import urlparse
from .www_66ip_cn import WWW_66IP_CN
from .ip_ihuan_me import IP_IHUAN_ME
from .ip_yqie_com import IP_YQIE_COM
from .www_89ip_cn import WWW_89IP_CN
from .www_data5u_com import WWW_DATA5U_COM
from .www_goubanjia_com import WWW_GOUBANJIA_COM
from .www_ip3366_net import WWW_IP3366_NET
from .www_kuaidaili_com import WWW_KUAIDAILI_COM
from .www_superfastip_com import WWW_SUPERFASTIP_COM
from .www_xicidaili_com import WWW_XICIDAILI_COM
from .www_xiladaili_com import WWW_XILADAILI_COM
from .www_xsdaili_com import WWW_XSDAILI_COM
from .www_zdaye_com import WWW_ZDAYE_COM


class ProxyFactory:

    def create(self, url, code='utf-8', **kwargs):
        netloc = self.__get_netloc(url)
        return eval(netloc)(url, code, **kwargs)

    def __get_netloc(self, url):
        result = urlparse(url)
        return result.netloc.replace('.', '_').upper()
