import unittest

from core.DockerStepReader import DockerStepReader

class DockerStepReaderTest(unittest.TestCase):
    def test_validLine_stepNumber(self):
        self.assertEqual(6, DockerStepReader("Step 6/18 : RUN apt-get -y build-dep wine").get_step_number())

    def test_validLine_numberOfSteps(self):
        self.assertEqual(18, DockerStepReader("Step 6/18 : RUN apt-get -y build-dep wine").get_number_of_steps())

    def test_validLine_stepName(self):
        self.assertEqual("RUN", DockerStepReader("Step 6/18 : RUN apt-get -y build-dep wine").get_step_name())

    def test_validLine_stepDetails(self):
        self.assertEqual("apt-get -y build-dep wine", DockerStepReader("Step 6/18 : RUN apt-get -y build-dep wine").get_details())

    def test_invalidLine(self):
        self.assertEqual(None, DockerStepReader("Reading state information...").get_step_number())
