import requests
from bs4 import BeautifulSoup


class AvtotochkiServiceCard:
    __service_card_link = ''

    def __init__(self, service_card_link):
        self.__service_card_link = service_card_link

    def get_service_website(self) -> str:
        service_card_link = self.__service_card_link
        response = requests.get(service_card_link)
        html_parser = BeautifulSoup(response.text, 'lxml')
        website_link_tag = html_parser.select_one('span[data-website]')
        if website_link_tag is None:
            raise Exception(service_card_link + ': не удалось найти ссылку на сайт сервиса')

        # достается не значение data-website, а сам текст чтобы не переходить по ссылке-посреднику
        website = website_link_tag.text
        return website
