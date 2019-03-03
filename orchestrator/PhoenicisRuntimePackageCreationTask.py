import datetime

from builders.BuilderStageReader import BuilderStageReader
from orchestrator.Task import Task
from packagers.PhoenicisRuntimeWinePackageCreator import PhoenicisRuntimeWinePackageCreator


class PhoenicisRuntimePackageCreationTask(Task):
    def __init__(self, operatingSystem: str, arch: str):
        self.phoencisRuntimePackager = PhoenicisRuntimeWinePackageCreator().with_output_callback(self._building_hook)
        self.operatingSystem = operatingSystem
        self.arch = arch
        self.builder_stage_reader = BuilderStageReader()

        Task.__init__(self)

    def description(self):
        return "Phoenicis Wine Runtime Package Creation: %s / %s" % (self.os, self.arch)

    def argument(self):
        return {
            "os": self.operatingSystem,
            "arch": self.arch
        }

    def get_progress(self):
        return self._progress

    def get_message(self):
        return self.builder_stage_reader.get_message()

    def set_progress(self, progress):
        self._progress = progress

    def handle(self):
        self.phoencisRuntimePackager.build(self.distribution, self.version, self.os, self.arch)

    def _building_hook(self, line):
        self.builder_stage_reader.feed(line)
        self.last_update_date = datetime.datetime.now()
        self.set_progress(self.builder_stage_reader.get_percentage_estimation())
