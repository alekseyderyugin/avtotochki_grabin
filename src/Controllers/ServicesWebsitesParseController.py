from src import AvtotochkiServices, TaskManager
from src import File
from src.ParseWebsitesWorker import ParseWebsitesWorker


class ServicesWebsitesParseControllers:

    def __init__(self, avtotochki: AvtotochkiServices, services_links_file: File, services_websites_file: File):
        self.avtotochki = avtotochki
        self.services_links_file = services_links_file
        self.services_websites_file = services_websites_file

    def run(self):
        links = self.services_links_file.read_literal_eval()

        task_manager = TaskManager(links)

        thread_task_list = task_manager.manage_tasks(10)

        workers = []
        i = 0
        for link in thread_task_list:
            worker = ParseWebsitesWorker(link)
            worker.setName('worker#' + str(i))
            workers.append(worker)
            worker.start()
            i += 1

        for worker in workers:
            worker.join()

        websites = []

        for worker in workers:
            websites += worker.get_result()

        self.services_websites_file.write(str(websites))
