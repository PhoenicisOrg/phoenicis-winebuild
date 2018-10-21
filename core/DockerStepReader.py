import re

class DockerStepReader:
    def __init__(self, line):
        self._line = line
        _docker_state_regex = r"Step ([1-9]*)/([1-9]*) : ([A-Z]*) (.+)*"
        self.groups = re.search(_docker_state_regex, line)

    def get_step_number(self):
        if(self.groups is None):
            return None

        return int(self.groups.group(1))

    def get_number_of_steps(self):
        if(self.groups is None):
            return None

        return int(self.groups.group(2))

    def get_percentage(self):
        if(self.groups is None):
            return None

        return int(self.get_step_number() * 100 / self.get_number_of_steps())

    def get_step_name(self):
        if(self.groups is None):
            return None

        return self.groups.group(3)

    def get_details(self):
        if(self.groups is None):
            return None

        return self.groups.group(4)

    def get_message(self):
        return self.get_step_name() + ": " + self.get_details()
