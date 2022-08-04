from src import AvtotochkiServices
from src import File


class ServicesListPageParseController:

    def __init__(self, avtotochki: AvtotochkiServices, services_links_file: File):
        self.avtotochki = avtotochki
        self.services_links_file = services_links_file

    def run(self):
        links = self.avtotochki.get_services_links()
        self.services_links_file.write(str(links))
