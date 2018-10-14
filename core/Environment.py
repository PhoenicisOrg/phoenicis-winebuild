from core.Process import run, run_and_return

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

    def get_id(self):
        return run_and_return(["docker", "images",  "-q", self.full_name()]).decode("utf-8").replace("\n", "")

    def state(self):
        if(self.get_id() == ""):
            return "NOT_READY"
        else:
            return "READY"

    def build(self):
        run(["docker", "build", "-t", self.full_name(), "-f", self.dockerfile_path(), "."])

    def clean(self):
        run(["docker", "rmi", self.full_name()])
