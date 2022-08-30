import requests

from loguru import logger
from pprint import pformat


class GetDataByRequests:
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    timeout = 5

    def __init__(self, timeout=None):
        self.timeout = timeout or self.timeout

    def get_data(self, url):
        logger.debug(f"Requesting <{url}> with headers <{self.headers}> and"
                     f" timeout <{self.timeout}>.")

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
        except Exception as e:
            logger.exception(f"Can not direct connect to <{url}>")
            # TODO: returning None in that case is not right
            return None

        logger.debug(f"Response headers: <{response.headers}>.")
        logger.debug(f"Response is <{response}>")
        try:
            if len(response.content) < 1024:
                logger.debug(f"Response content: \n{pformat(response.content)}")
        except:
            pass

        return response

    @property
    def headers(self):
        return {"User-Agent": self.USER_AGENT}
