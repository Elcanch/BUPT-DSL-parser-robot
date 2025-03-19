import unittest
from unittest.mock import patch
import Parser
import re
import Interpreter_fixed as Interpreter

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        # 初始化 Parser 和 Interpreter 对象
        self.parser = Parser.parser()
        # 模拟输入脚本
        self.parser.parseText("""
        Step step1
        Speak "Hello $name"
        Listen 5
        Branch Yes step2
        Branch Quit step3
        Silence step3
        Default step4
        Exit
        Step step3
        Exit
        """)
        self.interpreter = Interpreter.Interpreter(self.parser)

    def test_execSpeak_with_variable(self):
        # 设置变量并测试 execSpeak 方法
        self.parser.script.variables["name"] = "Elichen"
        text = "Hello $name"
        result = self.interpreter.execSpeak(text)
        self.assertEqual(result, "Hello Elichen")

    def test_execSpeak_without_variable(self):
        # 不设置变量，检查 execSpeak 方法
        text = "Hello World"
        result = self.interpreter.execSpeak(text)
        self.assertEqual(result, "Hello World")

    def test_execListen_with_user_input(self):
        # 使用模拟的用户输入来测试 execListen 方法
        self.interpreter.setUserInput("Yes")
        result = self.interpreter.execListen(5)
        self.assertEqual(result, "Yes")

    def test_execListen_without_user_input(self):
        # 没有用户输入，检查返回值
        self.interpreter.setUserInput(None)
        result = self.interpreter.execListen(5)
        self.assertEqual(result, "")

    @patch('builtins.print')
    def test_getNextStep_with_silence(self, mock_print):
        # 测试用户输入为 "silence" 时的行为
        self.interpreter.setUserInput("silence")
        next_step = self.interpreter.getNextStep("silence")
        self.assertEqual(next_step, "step3")  # Silence 指向 step3

    @patch('builtins.print')
    def test_getNextStep_with_branch(self, mock_print):
        # 测试用户输入与分支匹配时的行为
        self.interpreter.setUserInput("Yes")
        next_step = self.interpreter.getNextStep("Yes")
        self.assertEqual(next_step, "step2")  # Branch "Yes" 指向 step2

    @patch('builtins.print')
    def test_getNextStep_with_default(self, mock_print):
        # 测试没有匹配分支时使用默认分支
        self.interpreter.setUserInput("No")
        next_step = self.interpreter.getNextStep("No")
        self.assertEqual(next_step, "step4")  # Default 指向 step4

    @patch('builtins.print')
    def test_getNextStep_with_exit(self, mock_print):
        # 测试用户输入 "Quit" 时的行为
        self.interpreter.setUserInput("Quit")

        # 用户输入 Quit 时，应该跳转到 step3
        next_step = self.interpreter.getNextStep("Quit")
        self.assertEqual(next_step, "step3")  # Branch "Quit" 指向 step3
        self.interpreter.is_exit = True  # 设置 is_exit 为 True，表示退出程序
        # 确保 step3 执行 exit 后退出
        next_step = self.interpreter.getNextStep("Quit")  # 进入 step3 并执行 exit
        self.assertIsNone(next_step)  # Should exit, no next step

        # 确保打印了退出信息
        mock_print.assert_any_call("Exiting because is_exit is True")

    def test_execSpeak_removes_quotes(self):
        # 测试 execSpeak 是否正确去除引号
        text = '"Hello World"'
        result = self.interpreter.execSpeak(text)
        self.assertEqual(result, "Hello World")

    def test_execSpeak_with_multiple_variables(self):
        # 测试多个变量的替换
        self.parser.script.variables["name"] = "Elichen"
        self.parser.script.variables["place"] = "home"
        text = "Hello $name, welcome to $place!"
        result = self.interpreter.execSpeak(text)
        self.assertEqual(result, "Hello Elichen, welcome to home!")

if __name__ == "__main__":
    unittest.main()
