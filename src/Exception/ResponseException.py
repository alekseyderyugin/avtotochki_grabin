from requests import Response


class ResponseException(Exception):
    def __init__(self, response: Response):
        message = '{0}: получен недействительный код ответа - {1}'.format(response.url, response.status_code)
        super(ResponseException, self).__init__(message)
