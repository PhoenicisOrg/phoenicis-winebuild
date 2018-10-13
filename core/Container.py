from core.Process import run_and_return, run

class Container:
    @staticmethod
    def from_id(container_id):
        container = Container(None)
        container.container_id = container_id
        return container

    def __init__(self, environment):
        self.container_id = None
        self.environment = environment

    def start(self):
        self.container_id = run_and_return(["docker", "run",  "-dit", self.environment.full_name()]).decode("utf-8").replace("\n", "")

    def run(self, command, workdir = None):
        if(workdir is None):
            run(["docker", "exec", self.container_id] + command)
        else:
            run(["docker", "exec", "--workdir", workdir, self.container_id] + command)

    def get_file(self, file):
        run(["docker", "cp", self.container_id + ":" + file, "./"])

    def run_script(self, script):
        run(["docker", "cp", script, self.container_id + ":/tmp/script"])
        self.run(["bash", "/tmp/script"])

    def clean(self):
        run(["docker", "container", "kill", self.container_id])
        run(["docker", "rm", self.container_id])
