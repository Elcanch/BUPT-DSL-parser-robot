class Step:
    def __init__(self, stepID=None):
        self.stepID = stepID
        self.speak = None
        self.listen = None
        self.branch = {}
        self.silence = None
        self.default = None
        self.exit = None

    def set_speak(self, expression):
        self.speak = expression

    def set_listen(self, timeout):
        self.listen = (timeout)

    def set_branch(self, answer, next_stepID):
        self.branch[answer] = next_stepID

    def set_silence(self, next_stepID):
        self.silence = next_stepID

    def set_default(self, next_stepID):
        self.default = next_stepID

    def set_exit(self):
        self.exit = True

class Script:
    def __init__(self):
        self.mainStep = None
        self.steps = {}
        self.variables = {}
        self.success = True

    def create_step(self, stepId):
        step = Step(stepId)
        self.steps[stepId] = step
        return step
class ParserStub:
    def __init__(self):
        """
        初始化测试桩解析器，提供预定义的脚本结构
        """
        self.script = Script()
        self.script.variables = {
            'name': '',
            'balance': 0,
            'bill': 0,
            'charge': 0,
            'traffic': 0,
            'buy': 0
        }
        self._create_stub_script()

    def _create_stub_script(self):
        """
        创建一个模拟的 DSL 脚本结构
        """
        # 创建主步骤
        main_step = self.script.create_step('main')
        main_step.set_speak(f"欢迎使用DSL脚本系统！")
        main_step.set_listen(10)
        main_step.set_branch('yes', 'step1')
        main_step.set_branch('no', 'exit')
        main_step.set_silence('step1')
        main_step.set_default('step1')

        # 步骤1
        step1 = self.script.create_step('step1')
        step1.set_speak(f"请确认您的个人信息")
        step1.set_listen(10)
        step1.set_branch('confirm', 'step2')
        step1.set_branch('cancel', 'main')
        step1.set_silence('step2')
        step1.set_default('step2')

        # 步骤2
        step2 = self.script.create_step('step2')
        step2.set_speak(f"正在处理您的业务...")
        step2.set_listen(10)
        step2.set_branch('continue', 'step3')
        step2.set_branch('stop', 'exit')
        step2.set_silence('step3')
        step2.set_default('step3')

        # 步骤3
        step3 = self.script.create_step('step3')
        step3.set_speak(f"业务处理完成")
        step3.set_exit()

        # 退出步骤
        exit_step = self.script.create_step('exit')
        exit_step.set_speak(f"感谢使用，再见！")
        exit_step.set_exit()

        # 设置主步骤
        self.script.mainStep = main_step

    def parseText(self, text):
        """
        模拟解析文本脚本的方法
        
        Args:
            text (str): 输入的脚本文本
        """
        # 在实际测试中可以根据输入文本动态调整脚本
        print(f"Parsing text: {text}")
        self.script.success = True
        return self.script

    def parseFile(self, file_name):
        """
        模拟从文件解析脚本的方法
        
        Args:
            file_name (str): 脚本文件名
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"Parsing file: {file_name}")
                return self.parseText(content)
        except FileNotFoundError:
            print(f"文件 {file_name} 未找到")
            self.script.success = False
            return self.script

    def get_stub_script(self):
        """
        获取测试桩生成的脚本对象
        
        Returns:
            Script: 预定义的脚本对象
        """
        return self.script

def main():
    # 测试解析器测试桩
    parser_stub = ParserStub()
    
    # 测试 parseText 方法
    parser_stub.parseText("测试 DSL 脚本")
    
    # 测试 parseFile 方法（模拟）
    parser_stub.parseFile("/py/MyDsl/test.txt")
    
    # 获取脚本对象并打印详情
    script = parser_stub.get_stub_script()
    print("\n脚本变量:")
    for var, value in script.variables.items():
        print(f"{var}: {value}")
    
    print("\n脚本步骤:")
    for step_id, step in script.steps.items():
        print(f"步骤 {step_id}:")
        print(f"  Speak: {step.speak}")
        print(f"  Listen: {step.listen}")
        print(f"  分支: {step.branch}")
        print(f"  Exit: {step.exit}\n")
    interpreter = Interpreter(parser_stub)
    interpreter.execute()

import re
import Parser
class Interpreter:
    def __init__ (self,parser):
        self.parser = parser
        self.script = parser.script
        self.currentStep = self.script.mainStep
        self.variables = self.script.variables
        self.user_input = None  # 初始化用户输入变量
        self.is_exit = False  # 初始化退出标志

    def execute(self):
        while self.currentStep :
            response = ""

            if self.currentStep.speak:
                response = self.execSpeak(self.currentStep.speak)

            # 检查是否是退出步骤
            if self.currentStep.exit :
                self.is_exit = True
                break

            userInput = None
            if self.currentStep.listen:
                userInput = self.execListen(self.currentStep.listen)
                if userInput is None:
                    userInput = 'silence'

            if not self.currentStep:
                print('不合法的步骤产生，请检查脚本')
                break
            return response

    def execSpeak(self, text):
        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            if var_name in self.variables:
                return str(self.variables[var_name])
            return match.group(0)  # 如果变量未找到，返回原始匹配

        # 使用正则表达式替换变量，支持 $() 和 $ 两种语法
        text = re.sub(r'\$\((\w+)\)|\$(\w+)' ,replace_var, text)
        text = text.strip('"\'')
        text = text.replace('"', '')
        self.currentStep.speak = text
        print(text)
        return text

    def execListen(self,timeout):
        print(f" 开始监听{timeout}秒，请说话...")
        return self.user_input if self.user_input else ''            
        
    def setUserInput(self, user_input):
        self.user_input = user_input

    def getNextStep(self,userInput):
        print(f"用户输入：{userInput}")
        print(self.is_exit)
        if self.is_exit == True:
            print(f"is_exit:{self.is_exit}")
            print("Exiting because is_exit is True")
            return None
        
        if userInput == 'silence' or userInput == None:
            return self.currentStep.silence
        
        if userInput in self.currentStep.branch:
            return self.currentStep.branch[userInput]
        
        return self.currentStep.default # 如果没有匹配的分支，返回默认分支

if __name__ == '__main__':
    main()