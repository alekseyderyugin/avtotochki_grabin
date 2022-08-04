class UrlFormatter:
    __url = ''

    def __init__(self, url):
        self.__url = url

    def format(self):
        url = self.__url
        if not ('https://' in url or 'http://' in url):
            url = 'http://' + url

        return url.lower()