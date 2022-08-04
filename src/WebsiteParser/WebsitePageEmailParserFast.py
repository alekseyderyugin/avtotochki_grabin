from src.WebsiteParser import AbstractWebsitePageEmailParser


class WebsitePageEmailParserFast(AbstractWebsitePageEmailParser):
    def get_email_regex(self) -> str:
        return '''([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'''
