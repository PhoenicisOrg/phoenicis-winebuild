import threading

from orchestrator.Task import Task


class Orchestrator:
    def __init__(self):
        self._tasks = []
        self._semaphore = threading.Semaphore(2)

    def run_task(self, task: Task) -> None:
        self._tasks += [task]
        task.append_on_finish_event(lambda: self._when_task_is_terminated(task))
        task.append_on_error_event(lambda: self._when_task_is_onerror(task))
        task.append_on_start_event(lambda: self._when_task_is_started(task))
        task.start()

    def _when_task_is_started(self, task):
        self._semaphore.acquire()

    def _when_task_is_terminated(self, task):
        ## self._tasks.remove(task)
        self._semaphore.release()

    def _when_task_is_onerror(self, task):
        self._semaphore.release()

    def remove_task(self, task_id):
        tasks = []
        for task in self._tasks:
            if task["id"] != task_id:
                tasks += [task]
        self._tasks = tasks

    def tasks(self):
        tasks = []
        for task in self._tasks:
            tasks += [{
                "id": task.id(),
                "description": task.description(),
                "argument": task.argument(),
                "type": task.type(),
                "status": task.status,
                "message": task.get_message(),
                "running": task.running,
                "progress": task.get_progress(),
                "start_date": task.start_date,
                "last_update_date": task.last_update_date,
                "end_date": task.end_date
            }]
        return tasks


default_orchestrator = Orchestrator()
