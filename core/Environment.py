from core.Process import run

class Environment:
    def __init__(self, name, os, arch):
        self.name = name
        self.os = os
        self.arch = arch

    def full_name(self):
        instance = ":".join([self.os + "-" + self.arch, self.name])
        return "/".join(["phoenicis", "winebuild", instance])

    def dockerfile_path(self):
        return "environments/" + "-".join([self.os, self.arch, self.name])

    def build(self):
        run(["docker", "build", "-t", self.full_name(), "-f", self.dockerfile_path(), "."])
