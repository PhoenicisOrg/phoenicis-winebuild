from orchestrator.Task import Task

class Orchestrator:
    def __init__(self):
        self._tasks = []

    def run_task(self, task: Task) -> None:
        self._tasks += [task]
        task.append_on_finish_event(lambda: self._when_task_is_terminated(task))
        task.start()

    def _when_task_is_terminated(self, task):
        self._tasks.remove(task)

    def tasks(self):
        tasks = []
        for task in self._tasks:
            tasks += [{
                "id": task.id(),
                "description": task.description(),
                "argument": task.argument(),
                "type": task.type(),
                "running": task.running,
                "progress": task.get_progress(),
                "start_date": task.start_date,
                "last_update_date": task.last_update_date,
                "end_date": task.end_date
            }]
        return tasks;
