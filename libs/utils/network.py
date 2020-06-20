import requests

from libs.utils.logger import Logger

import pprint

pp = pprint.PrettyPrinter(indent=4, depth=10, width=128)


class GetDataByRequests(metaclass=Logger):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    proxies_list = []
    response = None

    def set_proxies(self, proxies=None):
        """
        type proxies: list or tuple of dicts
        proxies obj must be like:
            [{'proxy_type': 'socks5',
              'user': 'user_name',
              'passwd': 'user_password',
              'host': 'proxy_host',
              'port': 'proxy_port' }, ]
        TODO need improve to more flexible
        """
        if not proxies:
            return False

        pattern = '{proxy_type}://{user}:{passwd}@{host}:{port}/'
        self.proxies_list = [
            {
                'http': pattern.format(**proxy),
                'https': pattern.format(**proxy)
            }
            for proxy in proxies
        ]

    def get_data(self, url, user_agent=None):
        self.response = None

        user_agent = user_agent if user_agent else self.USER_AGENT
        headers = {'User-Agent': user_agent}

        try:
            self.response = requests.get(url, headers=headers, timeout=5, )
        except Exception as e:
            exc_info = e.__reduce__()
            self.logger.debug('Can not direct connect to <%s>\n<%s> <%s>', url, exc_info[0], exc_info[1])
            if self.proxies_list:
                for proxy in self.proxies_list:
                    try:
                        self.response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
                    except:
                        self.logger.debug(
                            'Can not through proxy connect to <%s>\n<%s> <%s>',
                            url, exc_info[0], exc_info[1]
                        )
                    else:
                        break

        if self.response:
            return self.response
        else:
            return False

    def log_data(self):
        self.logger.info(pp.pformat(self.response))
