import time
from src.Controllers.ServicesListPageParseController import ServicesListPageParseController
from src.Controllers.ServicesWebsitesParseController import ServicesWebsitesParseControllers
from src.Controllers.WebsitesParseController import WebsitesParseController
from src import File, AvtotochkiServices


class Main:
    SITEMAP_URL_LIMIT = 30
    MAX_WORKERS_COUNT = 10

    @staticmethod
    def main():
        avtotochki = AvtotochkiServices()

        print('____AVTOTOCHKI_GRABING____')
        main_template = File('resources/templates/main.txt').read()

        services_links_file = File('data/services_links.txt')
        services_websites_file = File('data/services_websites.txt')

        actions = {
            '1': ServicesListPageParseController(avtotochki, services_links_file),
            '2': ServicesWebsitesParseControllers(avtotochki, services_links_file, services_websites_file),
            '3': WebsitesParseController(services_websites_file)
        }
        while True:
            command = input(main_template)

            if command in actions:
                controller = actions.get(command)
                controller.run()
            else:
                break


start_time = time.time()
Main.main()
print("--- %s секунд ---" % round((time.time() - start_time), 2))
