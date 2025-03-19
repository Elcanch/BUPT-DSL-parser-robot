'''
Author: Elichen 2954855725@qq.com
Date: 2024-12-14 10:43:27
LastEditors: Elichen 2954855725@qq.com
LastEditTime: 2024-12-17 17:05:40
FilePath: \code\py\MyDsl\Interpreter_fixed.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
import Parser
class Interpreter:
    def __init__ (self,parser):
        """
        初始化解释器
        
        参数:
        parser (Parser): 解析器对象，包含已解析的脚本信息
        
        属性:
        - parser: 解析器对象
        - script: 解析后的脚本对象
        - currentStep: 当前执行的步骤
        - variables: 脚本中定义的变量
        - user_input: 用户输入
        - is_exit: 对话是否结束的标志
        """
        self.parser = parser
        self.script = parser.script
        self.currentStep = self.script.mainStep
        self.variables = self.script.variables
        self.user_input = None  # 初始化用户输入变量
        self.is_exit = False  # 初始化退出标志

    def execute(self):
        """
        执行脚本的主方法
        
        主要功能:
        - 遍历并执行每个步骤
        - 处理对话步骤的说话和监听逻辑
        - 检测对话是否结束
        
        返回:
        str: 当前步骤的响应文本
        """
        while self.currentStep :
            response = ""

            # 执行当前步骤的说话部分
            if self.currentStep.speak:
                response = self.execSpeak(self.currentStep.speak)

            # 检查是否是退出步骤
            if self.currentStep.exit :
                self.is_exit = True
                break

            # 处理监听逻辑
            userInput = None
            if self.currentStep.listen:
                userInput = self.execListen(self.currentStep.listen)
                if userInput is None:
                    userInput = 'silence'

            # 检查步骤的有效性
            if not self.currentStep:
                print('不合法的步骤产生，请检查脚本')
                break
            return response

    def execSpeak(self, text):
        """
        执行文本输出，并替换变量
        
        参数:
        text (str): 要处理的文本
        
        主要功能:
        - 使用正则表达式替换变量
        - 支持 $() 和 $ 两种变量语法
        - 清理文本格式
        
        返回:
        str: 处理后的文本
        """
        def replace_var(match):
            # 内部函数：替换变量
            var_name = match.group(1) or match.group(2)
            if var_name in self.variables:
                return str(self.variables[var_name])
            return match.group(0)  # 如果变量未找到，返回原始匹配

        # 使用正则表达式替换变量，支持 $() 和 $ 两种语法
        text = re.sub(r'\$\((\w+)\)|\$(\w+)' ,replace_var, text)
        text = text.strip('"\'')
        text = text.replace('"', '')
        # 更新当前步骤的说话内容
        self.currentStep.speak = text
        print(text)
        return text

    def execListen(self,timeout):
        """
        执行监听用户输入逻辑
        
        参数:
        timeout (float): 监听的超时时间
        
        返回:
        str: 用户输入（如果有）
        """
        print(f" 开始监听{timeout}秒，请说话...")
        return self.user_input if self.user_input else ''            
        
    def setUserInput(self, user_input):
        """
        设置用户输入，用于将前端返回的输入存储到user_input变量中
        
        参数:
        user_input (str): 用户的输入内容
        """
        self.user_input = user_input

    def getNextStep(self,userInput):
        """
        根据用户输入确定下一个步骤
        
        参数:
        userInput (str): 用户的输入
        
        返回:
        str/None: 下一个步骤的标识符，如果对话结束则返回 None
        
        处理逻辑:
        - 检查是否已经退出
        - 处理静默场景
        - 匹配分支条件
        - 返回默认分支
        """
        print(f"用户输入：{userInput}")
        print(self.is_exit)
        if self.is_exit == True:
            # 检查是否已经退出
            print(f"is_exit:{self.is_exit}")
            print("Exiting because is_exit is True")
            return None
        # 处理静默场景
        if userInput == 'silence' or userInput == None:
            return self.currentStep.silence
        # 匹配分支条件
        if userInput in self.currentStep.branch:
            return self.currentStep.branch[userInput]
        # 返回默认分支
        return self.currentStep.default # 如果没有匹配的分支，返回默认分支
