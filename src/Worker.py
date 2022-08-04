import threading

from src import UrlFormatter, WebsiteSitemap, SitemapPagesEmailParser, RobotsFileParser

from src import File


class Worker(threading.Thread):
    result = []
    errors = []

    def __init__(self, websites: list, sitemap_url_limit: int):
        super().__init__()
        self.__websites = websites
        self.__sitemap_url_limit = sitemap_url_limit

    def run(self):
        for website in self.__websites:
            website_url = UrlFormatter(website).format()
            try:
                robots_parser = RobotsFileParser(website_url)
                sitemap_url = robots_parser.get_sitemap_url()
                sitemap = WebsiteSitemap(sitemap_url)
                try:
                    if sitemap.is_sitemap_index():
                        sitemap_of_index_urls = sitemap.get_sitemaps_of_index_urls()
                        sitemap_of_index = WebsiteSitemap(sitemap_of_index_urls[0])
                        pages_urls = sitemap_of_index.get_sitemap_urls(self.__sitemap_url_limit)
                    else:
                        pages_urls = sitemap.get_sitemap_urls(self.__sitemap_url_limit)
                except Exception as e:
                    msg = str(e) + '[использована главная страница]'
                    self.errors.append(msg)
                    print(msg)
                    pages_urls = [website_url]

                email_list = SitemapPagesEmailParser(pages_urls).get_emails(lazy_mode=True)
                self.result += email_list
                for email in email_list:
                    msg = website_url + ' ' + email
                    print(msg)

            except Exception as e:
                msg = str(e)
                self.errors.append(msg)
                print(msg)

    def get_result(self):
        return self.result

    def get_errors(self):
        return self.errors