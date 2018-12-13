import pycurl
import certifi
import logging

from io import BytesIO


class CurlGetter:
    def __init__(self, url, logger=None, proxies=None):
        self.url = url
        self.logger = logger if logger else self.__get_logger

        self.__set_proxies(proxies)

    @property
    def __get_logger(self, ):
        if not self.logger:
            logger = logging.getLogger()
            logger.setLevel(level=logging.DEBUG)
            hndlr = logging.StreamHandler()
            logger.addHandler(hndlr)

            return logger
        else:
            return self.logger

    def __init_curl(self, ):
        self.buffer = BytesIO()
        self.__curl = pycurl.Curl()
        self.__curl.setopt(self.__curl.URL, self.url)
        self.__curl.setopt(self.__curl.WRITEDATA, self.buffer)
        self.__curl.setopt(self.__curl.CAINFO, certifi.where())
        self.__curl.setopt(self.__curl.TIMEOUT, 5)
        self.__curl.setopt(self.__curl.VERBOSE, True)
        self.__curl.setopt(self.__curl.DEBUGFUNCTION,
                           self.__logger_wrapper(self.logger.debug))
        self.response = None

    @staticmethod
    def __logger_wrapper(func):
        def wrapper(debug_type, debug_msg, ):
            func("pycurl_debug(%d): %s" % (
            debug_type, debug_msg.decode('utf8').strip('\n')))

        return wrapper

    def __set_proxies(self, proxies):
        self.__proxies = [
            {'host': '%s:%s' % (proxy.server, proxy.port),
             'proxy_type': proxy.proxy_type,
             'proxy_auth': '%s:%s' % (proxy.user, proxy.passwd), }
            for proxy in proxies] if proxies else None

    def __use_proxy(self, err_code=None):
        self.__curl.setopt(self.__curl.SSL_VERIFYPEER,
                           0 if err_code == 60 else 1)

        for proxy in self.__proxies:
            #TODO make it not like shitty code
            if self.__proxy_perform(proxy, err_code):
                return True

    def __proxy_perform(self, proxy, err_code=None):
        self.__curl.setopt(self.__curl.PROXY, proxy['host'])
        if proxy['proxy_type'] == 'http':
            self.__curl.setopt(self.__curl.PROXYTYPE,
                               self.__curl.PROXYTYPE_HTTP)
        elif proxy['proxy_type'] == 'socks5':
            self.__curl.setopt(self.__curl.PROXYTYPE,
                               self.__curl.PROXYTYPE_SOCKS5)
        elif proxy['proxy_type'] == 'socks4':
            self.__curl.setopt(self.__curl.PROXYTYPE,
                               self.__curl.PROXYTYPE_SOCKS4)

        self.__curl.setopt(self.__curl.PROXYUSERPWD, proxy['proxy_auth'])

        try:
            self.__curl.perform()
        except Exception as e:
            if not err_code and e.args[0] == 60:
                self.logger.debug(
                    'Can not verify ssl. Trying skip verification. domain=<%s>',
                    self.url)
                if self.__use_proxy(err_code=e.args[0]):
                    return True
            elif not err_code:
                self.logger.debug(
                    'Can not through proxy connect. domain=<%s> Due to: <%s>',
                    self.url, e)
            elif err_code == 60:
                self.logger.debug(
                    'Can not through proxy connect without verification. domain=<%s> Due to: <%s>',
                    self.url, e)
        else:
            return True

        return False

    def get(self, ):
        self.__init_curl()
        try:
            self.__curl.perform()
        except Exception as e:
            self.logger.exception("Error")
            if self.__proxies:
                self.__use_proxy()
        self.__curl.close()
        self.response = self.buffer.getvalue().decode('utf-8')
        self.buffer.close()
