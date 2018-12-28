import json
import os


class ConfigurationReader:
    def _config(self, config_file):
        with open(config_file, 'r') as config_file_content:
            return json.load(config_file_content)

    def read(self, file):
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config",
                                   file + ".json")

        return self._config(config_file)
