

class TaskManager:
    __tasks = []

    def __init__(self, tasks: list):
        self.__tasks = tasks

    def manage_tasks(self, max_thread_count: int) -> list:
        threads_task_list = []

        for i in range(max_thread_count):
            threads_task_list.append([])

        tasks_iterator = iter(self.__tasks)
        task = self.__get_next_iterator_elem(tasks_iterator)
        while task:
            for i in range(max_thread_count):
                threads_task_list[i].append(task)
                task = self.__get_next_iterator_elem(tasks_iterator)
                if task is None:
                    break

        return threads_task_list

    def __get_next_iterator_elem(self, iterator):
        try:
            elem = next(iterator)
            return elem
        except StopIteration:
            return None
