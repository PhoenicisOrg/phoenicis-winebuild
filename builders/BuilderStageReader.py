import re

class BuilderStageReader:
    def __init__(self):
        self._current_stage = 0
        self._current_step = 0
        self._max_stage = 0
        self._max_step = 0
        self._message = ""
        self._percentage = 0
        self._stage_message = ""
        self._step_message = ""

    def feed(self, line):
        if(line.startswith("[END]")):
            self._percentage = 100
            return

        step_regex = r"\[(STAGE|STEP) ([0-9]+)\/([0-9]+)\] (.+)*"
        step_result = re.search(step_regex, line)

        if(step_result is None):
            return

        if(step_result.group(1) == "STAGE"):
            self._current_stage = int(step_result.group(2))
            self._max_stage = int(step_result.group(3))
            self._stage_message = step_result.group(4)
            self._current_step = 0
            self._max_step = 0

        if(step_result.group(1) == "STEP"):
            self._current_step = int(step_result.group(2))
            self._max_step = int(step_result.group(3))
            self._step_message = step_result.group(4)

        self.estimate_percentage()

    def get_step_message(self):
        return self._step_message

    def get_stage_message(self):
        return self._stage_message

    def estimate_percentage(self):
        if(self._max_stage != 0):
            percentage_size_of_stage = 100 / self._max_stage

            if(self._current_step != 0):
                step_increment = percentage_size_of_stage * self._max_step / self._current_step
            else:
                step_increment = 0
            self._percentage = (self._current_stage - 1) * percentage_size_of_stage + step_increment

    def get_percentage_estimation(self):
        return self._percentage
