import datetime

from core.DockerStepReader import DockerStepReader
from core.Environment import Environment
from orchestrator.Task import Task


class EnvironmentCreationTask(Task):
    def __init__(self, environment: Environment):
        self.environment: Environment = environment
        self._progress: int = 0
        self._message: str = ""
        super().__init__()

    def description(self):
        return "Environment creation: " + self.environment.full_name()

    def argument(self):
        return {
            "docker_name": self.environment.full_name()
        }

    def get_progress(self):
        return self._progress

    def set_progress(self, progress):
        self._progress = progress

    def handle(self):
        self.environment.build(callback = self._building_hook)

    def get_message(self):
        return self._message

    def _building_hook(self, line):
        step_reader = DockerStepReader(line)
        percentage = step_reader.get_percentage()
        self.last_update_date = datetime.datetime.now()
        if percentage is not None:
            self.set_progress(percentage)
            self._message = step_reader.get_message()
