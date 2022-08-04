from bs4 import BeautifulSoup
import requests
from requests import Response

from src import File
from src.AvtotochkiServicePreviewCard import AvtotochkiServicePreviewCard
from src.AvtotochkiServiceCard import AvtotochkiServiceCard


class AvtotochkiServices:
    SERVICES_MAIN_PAGE_URL = 'http://avtotochki.ru/catalog/avtoservisy/pt1c1657912419996/'

    def make_main_page_request(self) -> Response:
        return self.make_request(self.SERVICES_MAIN_PAGE_URL)

    def make_request(self, url) -> Response:
        request_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate,  br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        return requests.get(url=url, headers=request_headers)

    def get_services_links(self) -> list:
        links = []

        page_num = 1
        while True:
            url = self.SERVICES_MAIN_PAGE_URL + str(page_num)

            page_links = self.__get_services_list_page_links(url)

            for link in page_links:
                if link in links:
                    page_links.remove(link)

            if not page_links or page_num == 145:
                print('Ссылки получены')
                break
            links += page_links
            print('Страница ' + str(page_num) + ': получено')
            page_num += 1

        return links

    def __get_services_list_page_links(self, url):
        response = self.make_request(url)
        html = str(response.text)
        parser = BeautifulSoup(html, 'lxml')
        page_links = []
        div = parser.find('div', {'class': 'poiCatalogBlock'})
        if div is None:
            return page_links
        services_links_container = div.find('ol', {'class': 'poiList listColumns2'})

        if services_links_container is None:
            return page_links

        services_links_tags = services_links_container.select('li > a')

        for tag in services_links_tags:
            link = tag.get('href')
            page_links.append(link)
        return page_links

    def get_services_websites_from_links(self, service_preview_card_links) -> list:
        service_websites = []
        for service_preview_url in service_preview_card_links:
            try:
                service_preview_card = AvtotochkiServicePreviewCard(service_preview_url)
                try:
                    service_card_url = service_preview_card.get_service_card_url()
                except Exception:
                    service_card_url = service_preview_url

                service_card = AvtotochkiServiceCard(service_card_url)
                website = service_card.get_service_website()

                if website not in service_websites:
                    service_websites.append(website)
                    print(service_preview_url + ': вебсайт получен')

            except Exception as e:
                print(str(e))
                continue

        return service_websites


    def __service_card_preview_get_card_link(self, link: str) -> str:
        response = self.make_request(link)
        html_parser = BeautifulSoup(response.text, 'lxml')

        card_link_selector = 'div[class="mainInfo"] > a[class="name"]'
        service_card_link_tag = html_parser.select_one(card_link_selector)

        if service_card_link_tag is None:
            raise Exception(link + ': не удалось найти ссылку на карточку сервиса')

        return service_card_link_tag.get('href')

