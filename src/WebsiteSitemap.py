import requests
from bs4 import BeautifulSoup, Tag

from src import UrlException, ResponseException


class WebsiteSitemap:
    sitemap_url = ''
    sitemap_parser = None
    index_sitemaps_tags = []

    def __init__(self, url):
        self.sitemap_url = url
        sitemap_url = self.sitemap_url
        try:
            response = requests.get(sitemap_url, timeout=5)
        except requests.exceptions.ReadTimeout:
            raise UrlException(sitemap_url, 'не удалось получить файл sitemap')

        if not response.ok:
            raise ResponseException(response)
        xml = response.text
        self.sitemap_parser = BeautifulSoup(xml, 'lxml')

    def is_sitemap_index(self) -> bool:
        self.index_sitemaps_tags = self.sitemap_parser.select('sitemap')
        return bool(self.index_sitemaps_tags)

    def get_sitemaps_of_index_urls(self) -> list:
        sitemaps_urls_tags = self.sitemap_parser.select('sitemap > loc')
        return self.__get_tags_text(sitemaps_urls_tags)

    def get_sitemap_urls(self, limit) -> list:
        url_tags = self.sitemap_parser.select('url > loc', limit=limit)
        if not url_tags:
            raise UrlException(self.sitemap_url, 'sitemap не содержит ссылок, либо имеет неверный формат')

        return self.__get_tags_text(url_tags)

    def __get_tags_text(self, tag_list: list) -> list:
        tags_text_list = []
        for tag in tag_list:
            tags_text_list.append(tag.text)
        return tags_text_list
