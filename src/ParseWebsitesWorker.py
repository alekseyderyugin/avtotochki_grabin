import threading

from src import AvtotochkiServicePreviewCard, AvtotochkiServiceCard


class ParseWebsitesWorker(threading.Thread):
    result = []

    def __init__(self, service_preview_card_links):
        super().__init__()
        self.service_preview_card_links = service_preview_card_links

    def run(self):
        service_websites = []
        for service_preview_url in self.service_preview_card_links:
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

        self.result = service_websites

    def get_result(self) -> list:
        return self.result
