from src.WebsiteParser import WebsitePageEmailParserFast


class SitemapPagesEmailParser:
    __urls = []

    def __init__(self, sitemap_urls: list):
        self.__urls = sitemap_urls

    def get_emails(self, lazy_mode: bool = False) -> list:
        emails = []
        for url in self.__urls:
            try:
                page_email_list = WebsitePageEmailParserFast(url).get_emails()
                if page_email_list:
                    if lazy_mode is True:
                        emails = page_email_list
                        break
                    else:
                        emails = emails + page_email_list
            except Exception:
                continue
        return list(set(emails))
