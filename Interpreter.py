import queue
import Parser
import threading
import re
import os

class Interpreter:
    def __init__ (self,parser):
        self.parser = parser
        self.script = parser.script
        self.currentStep = self.script.mainStep
        self.variables = self.script.variables
        self.user_input = None  # 初始化用户输入变量

        self.initialize_variables()
    
    def initialize_variables(self):
        print("欢迎使用DSL脚本系统！")
        while True:
            name = input("请输入您的姓名：").strip()
            if name :
                break;
            print("姓名不能为空，请重新输入！")

        while True:
            try:
                balance = float(input("请输入您的余额："))
                if balance>=0 :
                    break;
                print("余额不能为负数！")
            except ValueError:
                print("请重新输入有效数字！")

         # 账单输入
        while True:
            try:
                bill = float(input("请输入当前账单金额："))
                if bill >= 0:
                    break
                print("账单金额不能为负数！")
            except ValueError:
                print("请重新输入有效数字！")

        # 流量费用输入
        while True:
            try:
                traffic = float(input("请输入本月流量费用："))
                if traffic >= 0:
                    break
                print("流量费用不能为负数！")
            except ValueError:
                print("请重新输入有效数字！")

        # 购买金额输入
        while True:
            try:
                buy = float(input("请输入本次购买金额："))
                if buy >= 0:
                    break
                print("购买金额不能为负数！")
            except ValueError:
                print("请重新输入有效数字！")

        # 充流量输入
        while True:
            try:
                charge = float(input("请输入充值流量(GB)："))
                if charge >= 0:
                    break
                print("充值流量不能为负数！")
            except ValueError:
                print("请重新输入有效数字！")

        self.variables['name'] = name
        self.variables['balance'] = balance
        self.variables['bill'] = bill
        self.variables['charge'] = charge
        self.variables['traffic'] = traffic
        self.variables['buy'] = buy

    
    def execute(self):
        while self.currentStep:
            if self.currentStep.speak:
                self.execSpeak(self.currentStep.speak)

            # 检查是否是退出步骤
            if self.currentStep.exit == True:
                break

            userInput = None
            if self.currentStep.listen:
                userInput = self.execListen(self.currentStep.listen)
                if userInput is None:
                    userInput = 'silence'
            # 获取下一步
            nextStepID = self.getNextStep(userInput)
            # 更新当前步骤
            self.currentStep = self.script.steps[nextStepID]

            if not self.currentStep:
                print('不合法的步骤产生，请检查脚本')
                break

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

    def execListen(self,time):
        try:
            print(f"Listening for {time} seconds")
            self.user_input = self.getInput(time)
            if self.user_input is None:
                return 'silence'
            return self.user_input
            
        except Exception as e:
            print(f"Error in listening: {e}")
            return None
    def getInput(self, time):
        input_queue = queue.Queue()
        # 创建输入线程
        def inputThread():
            try :
                input_queue.put(input("请输入: "))
            except:
                input_queue.put(None)

        thread = threading.Thread(target=inputThread)
        thread.start()
        # 等待输入
        thread.join(time)
        if thread.is_alive():
            return None
        return input_queue.get()
    
    def getNextStep(self,userInput):
        if userInput == 'silence':
            return self.currentStep.silence
        
        if userInput in self.currentStep.branch:
            return self.currentStep.branch[userInput]
        
        return self.currentStep.default # 如果没有匹配的分支，返回默认分支
    
if __name__ == '__main__':
    parser = Parser.parser()
    parser.parseFile("./py/MyDsl/test.txt")
    interpreter = Interpreter(parser)
    interpreter.execute()
    # print(interpreter.currentStep.branch)