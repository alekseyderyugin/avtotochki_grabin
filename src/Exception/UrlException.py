class UrlException(Exception):
    def __init__(self, url, message):
        super(UrlException, self).__init__(url + ' : ' + message)
