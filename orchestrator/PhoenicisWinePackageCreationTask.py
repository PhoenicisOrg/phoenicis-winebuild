import re, datetime

from orchestrator.Task import Task
from core.DockerStepReader import DockerStepReader
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator

class PhoenicisWinePackageCreationTask(Task):
    def __init__(self, distribution: str, version: str, os: str, arch: str):
        self.phoencisWinePackager = PhoenicisWinePackageCreator().with_output_callback(self._building_hook)
        self.distribution = distribution
        self.version = version
        self.os = os
        self.arch = arch
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

    def set_progress(self, progress):
        self._progress = progress

    def handle(self):
        self.phoencisWinePackager.build(self.distribution, self.version, self.os, self.arch)

    def _building_hook(self, line):
        # FIXME: Use this hook to estimate build percentage
        print("--> %s" % line, end = '')
        pass
