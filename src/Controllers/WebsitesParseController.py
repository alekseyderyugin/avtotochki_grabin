from src import File, TaskManager
from src.Worker import Worker
from src.WebsiteListSanitizeHelper import WebsiteListSanitizeHelper


class WebsitesParseController:
    SITEMAP_URL_LIMIT = 30
    MAX_WORKERS_COUNT = 2

    def __init__(self, services_websites_file: File):
        self.services_websites_file = services_websites_file

    def run(self):
        website_list = self.services_websites_file.read_literal_eval()
        website_list_sanitized = WebsiteListSanitizeHelper(website_list).sanitize()

        services_websites_sanitized_file = File('data/services_websites_sanitized.txt')
        services_websites_sanitized_file.write(str(website_list_sanitized))

        task_manager = TaskManager(website_list_sanitized)

        thread_task_list = task_manager.manage_tasks(self.MAX_WORKERS_COUNT)

        workers = []
        i = 0
        for website_list in thread_task_list:
            worker = Worker(website_list, self.SITEMAP_URL_LIMIT)
            worker.setName('worker#' + str(i))
            workers.append(worker)
            worker.start()
            i += 1

        for worker in workers:
            worker.join()

        result = []
        errors = []
        for worker in workers:
            emails = worker.get_result()
            result += emails
            errors += worker.get_errors()

        websites_emails_file = File('data/websites_emails.txt')
        websites_emails_file.write(str(result))
        websites_parse_email_errors_file = File('data/websites_parse_email_errors.txt')
        websites_parse_email_errors_file.write(str(errors))
        print("Email'ы получены")
