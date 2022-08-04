import re
import requests

from src import UrlException


class RobotsFileParser:
    website_url = ''

    def __init__(self, website_url):
        self.website_url = website_url

    def get_sitemap_url(self):
        response = requests.get(self.__get_robots_url())
        robots_command_list = response.text.split('\n')

        sitemap_url = ''
        sitemap_pattern = '''sitemap:(.*)'''
        for command in robots_command_list:
            match = re.search(sitemap_pattern, command.lower(), re.IGNORECASE)
            if match and match.groups():
                sitemap_url = match.groups()[0]
                sitemap_url = sitemap_url.strip()
                break

        if not sitemap_url:
            raise UrlException(self.website_url, 'не удалось получить sitemap')
        return sitemap_url

    def __get_robots_url(self) -> str:
        return self.website_url.rstrip('/') + '/robots.txt'
