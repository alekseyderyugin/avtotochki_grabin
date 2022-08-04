import requests
from bs4 import BeautifulSoup


class AvtotochkiServicePreviewCard:
    __service_preview_link = ''

    def __init__(self, service_preview_link):
        self.__service_preview_link = service_preview_link

    def get_service_card_url(self) -> str:
        link = self.__service_preview_link

        response = requests.get(link)
        html_parser = BeautifulSoup(response.text, 'lxml')

        card_link_selector = 'div[class="mainInfo"] > a[class="name"]'
        service_card_link_tag = html_parser.select_one(card_link_selector)

        if service_card_link_tag is None:
            raise Exception(link + ': не удалось найти ссылку на карточку сервиса')

        url = service_card_link_tag.get('href')
        return url
