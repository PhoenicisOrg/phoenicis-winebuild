import datetime

from builders.BuilderStageReader import BuilderStageReader
from orchestrator.Task import Task
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator


class PhoenicisWinePackageCreationTask(Task):
    def __init__(self, distribution: str, os: str, version: str, arch: str):
        self.phoencisWinePackager = PhoenicisWinePackageCreator().with_output_callback(self._building_hook)
        self.distribution = distribution
        self.version = version
        self.os = os
        self.arch = arch
        self.builder_stage_reader = BuilderStageReader()

        Task.__init__(self)

    def description(self):
        return "Phoenicis Wine Package Creation: %s / %s / %s / %s" % (self.distribution, self.version, self.os, self.arch)

    def argument(self):
        return {
            "os": self.os,
            "version": self.version,
            "arch": self.arch,
            "distribution": self.distribution
        }

    def get_progress(self):
        return self._progress

    def get_message(self):
        return self.builder_stage_reader.get_message()

    def set_progress(self, progress):
        self._progress = progress

    def handle(self):
        self.phoencisWinePackager.build(self.distribution, self.version, self.os, self.arch)

    def _building_hook(self, line):
        self.builder_stage_reader.feed(line)
        self.last_update_date = datetime.datetime.now()
        self.set_progress(self.builder_stage_reader.get_percentage_estimation())
