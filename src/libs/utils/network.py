import requests
from logging import getLogger

logger = getLogger(__name__)


class GetDataByRequests:
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

        try:
            self.response = self._perform_request(url)
        except Exception as e:
            logger.exception(f'Can not direct connect to <{url}>')
            if self.proxies_list:
                self._request_through_proxy(url)

        return self.response

    def _request_through_proxy(self, url):
        for proxy in self.proxies_list:
            try:
                self.response = self._perform_request(url, proxy)
            except:
                logger.exception(f'Can not through proxy connect to <{url}>.')
            else:
                break

    def _perform_request(self, url, proxies=None):
        return requests.get(url, headers=self.headers, timeout=5,
                            proxies=proxies)

    @property
    def headers(self):
        return {'User-Agent': self.USER_AGENT}

    def log_data(self):
        logger.info(f"Get response: <{self.response}>")
        pass
