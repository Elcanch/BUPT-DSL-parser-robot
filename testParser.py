import unittest
import Parser
class TestStep(unittest.TestCase):
    def setUp(self):
        # 每个测试之前都会执行的代码
        self.step = Parser.Step("step1")

    def test_set_speak(self):
        self.step.set_speak("Hello")
        self.assertEqual(self.step.speak, "Hello")

    def test_set_listen(self):
        self.step.set_listen(5)
        self.assertEqual(self.step.listen, 5)

    def test_set_branch(self):
        self.step.set_branch("Yes", "step2")
        self.assertEqual(self.step.branch["Yes"], "step2")

    def test_set_silence(self):
        self.step.set_silence("step3")
        self.assertEqual(self.step.silence, "step3")

    def test_set_default(self):
        self.step.set_default("step4")
        self.assertEqual(self.step.default, "step4")

    def test_set_exit(self):
        self.step.set_exit()
        self.assertTrue(self.step.exit)


class TestScript(unittest.TestCase):
    def setUp(self):
        # 每个测试之前都会执行的代码
        self.script = Parser.Script()

    def test_create_step(self):
        step = self.script.create_step("step1")
        self.assertIsInstance(step, Parser.Step)
        self.assertEqual(step.stepID, "step1")

    def test_create_step_multiple(self):
        step1 = self.script.create_step("step1")
        step2 = self.script.create_step("step2")
        self.assertIn("step1", self.script.steps)
        self.assertIn("step2", self.script.steps)


class TestParser(unittest.TestCase):
    def setUp(self):
        # 每个测试之前都会执行的代码
        self.parser = Parser.parser()

    def test_parse_text_step(self):
        text = """
        Step step1
        Speak "Hello"
        Listen 5
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertEqual(step.speak, '"Hello"')
        self.assertEqual(step.listen, 5)

    def test_parse_text_invalid_listen(self):
        text = """
        Step step1
        Listen invalid_value
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertIsNone(step.listen)  # Invalid timeout should result in None

    def test_parse_text_branch(self):
        text = """
        Step step1
        Branch Yes step2
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertIn("Yes", step.branch)
        self.assertEqual(step.branch["Yes"], "step2")

    def test_parse_text_default(self):
        text = """
        Step step1
        Default step2
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertEqual(step.default, "step2")

    def test_parse_text_silence(self):
        text = """
        Step step1
        Silence step3
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertEqual(step.silence, "step3")

    def test_parse_text_exit(self):
        text = """
        Step step1
        Exit
        """
        self.parser.parseText(text)
        step = self.parser.script.steps["step1"]
        self.assertTrue(step.exit)

    def test_parse_file(self):
        file_content = """
        Step step1
        Speak "Hello"
        Listen 5
        """
        with open("test_script.txt", "w", encoding="utf-8") as f:
            f.write(file_content)
        
        self.parser.parseFile("test_script.txt")
        step = self.parser.script.steps["step1"]
        self.assertEqual(step.speak, '"Hello"')
        self.assertEqual(step.listen, 5)


if __name__ == "__main__":
    unittest.main()
