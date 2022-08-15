import os

from todoist_api_python.api import TodoistAPI


class Todoist:

    @staticmethod
    def getTasksByLabelIds(labels):
        api = TodoistAPI(os.getenv('TODOIST_TOKEN'))

        try:
            tasks = api.get_tasks()

            tasks = [task for task in tasks if any(elem == labels for elem in task.label_ids)]
            return tasks
        except Exception as error:
            print(error)
