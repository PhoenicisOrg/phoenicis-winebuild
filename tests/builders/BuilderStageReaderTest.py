import unittest, os
from builders.BuilderStageReader import BuilderStageReader

class BuilderStageReaderTest(unittest.TestCase):
    def test_no_feed(self):
        builder_stage_reader = BuilderStageReader()
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())

    def test_feed_invalid_line_no_crash(self):
        builder_stage_reader = BuilderStageReader()
        builder_stage_reader.feed("InvalidLine")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())

    def test_validLine_stageNumber(self):
        builder_stage_reader = BuilderStageReader()
        builder_stage_reader.feed("[STAGE 1/1] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())

    def test_buildSimulation_onlyStage(self):
        builder_stage_reader = BuilderStageReader()
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 1/2] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 2/2] test2")
        self.assertEqual(50, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[END] end")
        self.assertEqual(100, builder_stage_reader.get_percentage_estimation())

    def test_buildSimulation_stageAndSteps(self):
        builder_stage_reader = BuilderStageReader()
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 1/4] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STEP 0/1] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STEP 1/1] test")
        self.assertEqual(25, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 4/4] test2")
        self.assertEqual(75, builder_stage_reader.get_percentage_estimation())

    def test_buildSimulation_withFixture(self):
        builder_stage_reader = BuilderStageReader()
        with open(os.path.dirname(__file__) + "/builderStageReaderTestFixture.txt", 'r') as file:
            for line in file.readlines():
                builder_stage_reader.feed(line)                
                self.assertTrue(builder_stage_reader.get_percentage_estimation() >= 0)
                self.assertTrue(builder_stage_reader.get_percentage_estimation() <= 100)


    def test_overflow_hasNoEffect(self):
        builder_stage_reader = BuilderStageReader()
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 1/4] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STEP 0/1] test")
        self.assertEqual(0, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STEP 2/1] test")
        self.assertEqual(25, builder_stage_reader.get_percentage_estimation())
        builder_stage_reader.feed("[STAGE 4/4] test2")
        self.assertEqual(75, builder_stage_reader.get_percentage_estimation())
