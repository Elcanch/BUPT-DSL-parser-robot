class Step:
    def __init__(self, stepID=None):
        """
        初始化步骤对象
        
        参数:
        stepID (str, 可选): 步骤的唯一标识符
        
        属性:
        - stepID: 步骤的唯一标识符
        - speak: 该步骤需要说的话（文本表达）
        - listen: 监听用户输入的超时时间
        - branch: 根据不同输入跳转到不同步骤的分支字典
        - silence: 静默状态下要跳转的步骤
        - default: 默认跳转的步骤
        - exit: 是否结束对话的标志
        """
        self.stepID = stepID
        self.speak = None
        self.listen = None
        self.branch = {}
        self.silence = None
        self.default = None
        self.exit = None

    def set_speak(self, expression):
        """
        设置当前步骤需要说的话
        
        参数:
        expression (str): 要说的文本表达
        """
        self.speak = expression

    def set_listen(self, timeout):
        """
        设置监听用户输入的超时时间
        
        参数:
        timeout (int/float): 等待用户输入的最长时间（秒）
        """
        self.listen = (timeout)

    def set_branch(self, answer, next_stepID):
        """
        根据特定输入设置分支跳转
        
        参数:
        answer (str): 触发分支的特定输入
        next_stepID (str): 输入匹配后跳转的下一个步骤ID
        """
        self.branch[answer] = next_stepID

    def set_silence(self, next_stepID):
        """
        设置静默状态下的跳转步骤
        
        参数:
        next_stepID (str): 静默时跳转的步骤ID
        """
        self.silence = next_stepID

    def set_default(self, next_stepID):
        """
        设置默认跳转的步骤
        
        参数:
        next_stepID (str): 默认情况下跳转的步骤ID
        """
        self.default = next_stepID

    def set_exit(self):
        """
        标记当前步骤为对话结束点
        将 exit 标志设置为 True
        """
        self.exit = True

class Script:
    def __init__(self):
        """
        初始化脚本对象
        
        属性:
        - mainStep: 对话的起始步骤
        - steps: 存储所有步骤的字典（stepID: Step对象）
        - variables: 对话过程中使用的变量存储
        - success: 脚本执行的成功标志
        """
        self.mainStep = None
        self.steps = {}
        self.variables = {}
        self.success = True

    def create_step(self, stepId):
        """
        创建新的步骤并添加到脚本中
        
        参数:
        stepId (str): 新步骤的唯一标识符
        
        返回:
        Step: 新创建的步骤对象
        """
        step = Step(stepId)
        self.steps[stepId] = step
        return step
    
class parser:
    def __init__(self) :
        """
        初始化解析器
        
        属性:
        - script: Script 对象，用于存储解析后的脚本信息
        - currentStep: 当前正在处理的步骤
        """

        self.script = Script()
        self.currentStep = None

    def parseText(self, text) :
        """
        解析文本形式的脚本
        
        参数:
        text (str): 包含脚本语言的文本内容
        
        处理逻辑:
        - 按行分割文本
        - 忽略空行和注释行
        - 逐行解析有效指令
        """
        lines = text.split('\n')
        for line in lines :
            line = line.strip()
            if line and not line.startswith('#'):
                self.parseLine(line)

    def parseFile(self, file_name) :
        """
        从文件中解析脚本
        
        参数:
        file_name (str): 脚本文件的路径
        
        处理逻辑:
        - 打开并读取文件
        - 忽略空行和注释行
        - 逐行解析有效指令
        """
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file :
                line = line.strip()
                if line and not line.startswith('#'):
                    self.parseLine(line)

    def parseLine(self, line) :
        """
        解析单行脚本指令
        
        参数:
        line (str): 单行脚本指令
        
        主要功能:
        - 处理变量声明
        - 识别变量类型（文本/数字）
        - 处理变量名称
        - 转换特殊标记
        """
        parts = line.split(' ')
        token = []
        for part in parts :
            if part.startswith('#') :  
                break
            # 处理变量声明
            if part.startswith('$'):
                var_name = part[1:]  # 去掉 '$' 符号，得到变量名
                if '(' in var_name and ')' in var_name:
                    # 如果有括号，提取括号中的数据类型
                    start_index = var_name.index('(')
                    end_index = var_name.index(')')
                    data_type = var_name[start_index + 1:end_index]  # 提取括号内的数据类型
                    data_name = var_name[:start_index]  # 去掉括号内的数据类型，得到变量名
                    if data_type == 'text' :
                        self.script.variables[data_name] = ""
                    else :
                        self.script.variables[data_name] = 0
                    part = '$' + data_name  # 更新标记
                else:
                    # 默认为数字类型
                    self.script.variables[var_name] = 0
                    part = '$' + var_name  # 更新标记
            token.append(part)
        # 处理解析后的标记
        self.ProcessTokens(token)
    
    def ProcessTokens(self, token) :
        """
        处理解析后的标记（指令）
        
        参数:
        token (list): 解析后的指令标记列表
        
        主要功能:
        - 识别并执行不同类型的指令
        - 处理步骤创建、对话逻辑等
        - 错误处理和状态管理
        """
        if len(token) < 1 :
            print("Invalid command structure")
            return
        
        command = token[0]
        try:
            # 使用模式匹配处理不同指令
            match command:
                case "Step" :
                    self.ProcessStep(token[1])
                case "Speak" :
                    self.ProcessSpeak(token[1:])
                case "Listen" :
                    # 检查超时参数的有效性
                    if len(token) < 2 or not token[1].isdigit():
                        self.script.success = False
                    self.ProcessListen(token[1])
                case "Branch" :
                    self.ProcessBranch(token[1], token[2])
                case "Silence" :
                    self.ProcessSilence(token[1])
                case "Default" :
                    self.ProcessDefault(token[1])
                case "Exit" :
                    self.ProcessExit()
                case _:
                    # 处理未知指令
                    print(f"Invalid command: {command}")
                    self.script.success = False
        except Exception as e:
            # 捕获并处理执行过程中的异常
            print(f"Exception while processing {command}: {e}")
            self.script.success = False

    def ProcessStep(self, stepID) :
        """
        创建新的步骤
        
        参数:
        stepID (str): 步骤的唯一标识符
        
        返回:
        Step: 创建的步骤对象
        
        主要功能:
        - 创建新步骤
        - 设置当前步骤
        - 如果是第一个步骤，设为主步骤
        """
        step = self.script.create_step(stepID)
        self.currentStep = step
        if self.script.mainStep is None:
            self.script.mainStep = step
        
        return step
    
    def ProcessSpeak(self, text) :
        """
        设置当前步骤的对话内容
        
        参数:
        text (list): 要说的文本
        
        主要功能:
        - 处理并清理文本
        - 移除特殊字符（+ 和 "）
        - 设置步骤的对话文本
        """
        expression = "".join(t for t in text if t != '+' and t != '"' ) 
        self.currentStep.set_speak(expression)    

    def ProcessListen(self, timeout) :
        """
        设置当前步骤的监听超时时间
        
        参数:
        timeout (str): 超时时间
        
        主要功能:
        - 转换超时时间为浮点数
        - 处理无效的超时值
        """
        try:
            timeout = float(timeout)
            self.currentStep.set_listen(timeout)
        except ValueError:
            print(f"Invalid timeout value: {timeout}")
            self.currentStep.set_listen(None)  # 设置为None

    def ProcessBranch(self, answer, stepID) :
        """
        设置步骤的分支跳转逻辑
        
        参数:
        answer (str): 触发分支的输入
        stepID (str): 跳转的目标步骤ID
        """
        self.currentStep.set_branch(answer, stepID)
    
    def ProcessSilence(self, stepID) :
        """
        设置静默状态下的跳转步骤
        
        参数:
        stepID (str): 静默时跳转的步骤ID
        """
        self.currentStep.set_silence(stepID)

    def ProcessDefault(self, stepID) :
        """
        设置默认跳转的步骤
        
        参数:
        stepID (str): 默认情况下跳转的步骤ID
        """
        self.currentStep.set_default(stepID)

    def ProcessExit(self) :
        """
        标记当前步骤为对话结束点
        设置退出标志
        """
        self.currentStep.set_exit()