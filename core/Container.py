from core.Process import run_and_return, run

class Container:
    def __init__(self, environment):
        self.container_id = None
        self.environment = environment

    def start(self):
        self.container_id = run_and_return(["docker", "run",  "-dit", self.environment.full_name()]).decode("utf-8").replace("\n", "")

    def run(self, command):
        run(["docker", "exec", self.container_id] + command)

    def run_script(self, script):
        run(["docker", "cp", script, self.container_id + ":/tmp/script"])
        self.run(["bash", "/tmp/script"])

    def clean(self):
        run(["docker", "container", "kill", self.container_id])
        run(["docker", "rm", self.container_id])
