from urllib.parse import urlparse


class WebsiteListSanitizeHelper:
    website_list = []

    def __init__(self, website_list):
        self.website_list = website_list

    def sanitize(self):
        result = []
        for current_website in self.website_list:
            url_parser = urlparse(current_website)
            host = url_parser.hostname or current_website
            host = host.lower()
            if host not in result:
                result.append(host)

        return result
