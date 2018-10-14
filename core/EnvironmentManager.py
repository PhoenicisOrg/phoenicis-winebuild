import os, json
from core.Environment import Environment

class EnvironmentManager:
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config", "supported_environments.json")

    def __init__(self):
        self.load()

    def _config(self):
        with open(self.__class__.CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)

    def load(self):
        environments = self._config()
        loaded_environments = []
        for environment in environments:
            instance = Environment(environment["name"], environment["os"], environment["arch"])
            environment["docker_name"] = instance.full_name()
            environment["state"] = instance.state()
            
            loaded_environments += [{
                "instance": instance,
                "environment": environment
            }]

        self.environments = loaded_environments

    def list(self):
        return self.environments
