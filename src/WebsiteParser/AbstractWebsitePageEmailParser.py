import re
from abc import abstractmethod
import requests
from src import UrlException, ResponseException


class AbstractWebsitePageEmailParser:
    __url = ''

    def __init__(self, url: str):
        self.__url = url

    def get_emails(self) -> list:
        response = requests.get(self.__url)
        if not response.ok:
            raise ResponseException(response)
        html = response.text

        regex_email_pattern = self.get_email_regex()

        matches = re.findall(regex_email_pattern, html, re.IGNORECASE)
        if matches is None:
            raise UrlException(self.__url, 'не удалось найти email')

        return matches

    @abstractmethod
    def get_email_regex(self) -> str:
        pass
