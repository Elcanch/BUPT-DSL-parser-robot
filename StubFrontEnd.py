import requests
import json
import time

class DSLFrontendStub:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_step = None
        self.variables = {}

    def upload_script(self, script_content):
        """模拟上传DSL脚本"""
        url = f"{self.base_url}/upload"
        payload = {"input": script_content}
        
        try:
            response = self.session.post(url, json=payload)
            result = response.json()
            
            print(f"Script Upload Response: {result}")
            return result['response'] == "DSL 脚本文件上传成功！"
        except Exception as e:
            print(f"Script Upload Error: {e}")
            return False

    def initialize_variables(self, variables):
        """初始化DSL系统变量"""
        url = f"{self.base_url}/initialize"
        
        try:
            response = self.session.post(url, json=variables)
            result = response.json()
            
            print(f"Initialize Variables Response: {result}")
            self.variables = result.get('variables', {})
            return result
        except Exception as e:
            print(f"Initialize Variables Error: {e}")
            return None

    def simulate_interaction(self, user_inputs):
        """模拟用户交互流程"""
        interactions = []
        
        for user_input in user_inputs:
            url = f"{self.base_url}/process"
            payload = {"input": user_input}
            
            try:
                response = self.session.post(url, json=payload)
                result = response.json()
                
                print(f"User Input: {user_input}")
                print(f"Server Response: {result}")
                
                interactions.append({
                    'user_input': user_input,
                    'response': result.get('response', ''),
                    'next_step': result.get('next_step', ''),
                    'is_exit': result.get('is_exit', False)
                })
                
                self.current_step = result.get('next_step')
                
                # 如果退出，则停止交互
                if result.get('is_exit', False):
                    break
                
                # 模拟超时等待
                timeout = result.get('timeout', 0)
                time.sleep(timeout / 1000)
                
            except Exception as e:
                print(f"Interaction Error: {e}")
                break
        
        return interactions

    def get_initial_data(self):
        """获取初始数据"""
        url = f"{self.base_url}/dataInit"
        
        try:
            response = self.session.post(url)
            result = response.json()
            
            print(f"Initial Data: {result}")
            return result.get('variables', {})
        except Exception as e:
            print(f"Initial Data Error: {e}")
            return {}

class DSLFrontendStubDemo:
    @staticmethod
    def scenario_1_basic_interaction():
        """
        基本交互场景：查询余额和退出
        """
        print("\n=== 场景1：基本交互流程 ===")
        stub = DSLFrontendStub()
        
        # 上传DSL脚本
        script_content = """
        Step welcome
        Speak $name + "您好，欢迎查询"
        Listen 10
        Branch 查余额 balanceProc
        Branch 退出 exitProc

        Step balanceProc
        Speak "您的余额是" + $balance + "元"
        Listen 5
        Branch 退出 exitProc

        Step exitProc
        Speak "感谢使用，再见"
        Exit
        """
        
        if stub.upload_script(script_content):
            # 初始化变量
            initial_vars = {
                "name": {"value": "张先生", "type": "text"},
                "balance": {"value": 1000, "type": "number"}
            }
            stub.initialize_variables(initial_vars)
            
            # 模拟用户交互
            user_inputs = ["查余额", "退出"]
            interactions = stub.simulate_interaction(user_inputs)
            
            print("\n交互详情:")
            for interaction in interactions:
                print(f"用户输入: {interaction['user_input']}")
                print(f"系统响应: {interaction['response']}")

    @staticmethod
    def scenario_2_complex_interaction():
        """
        复杂交互场景：多步骤流程
        """
        print("\n=== 场景2：复杂交互流程 ===")
        stub = DSLFrontendStub()
        
        # 上传更复杂的DSL脚本
        script_content = """
        Step welcome
        Speak $name + "您好，欢迎使用服务"
        Listen 10
        Branch 查询 queryProc
        Branch 投诉 complainProc
        Branch 退出 exitProc

        Step queryProc
        Speak "请选择查询类型：账单/流量/余额"
        Listen 10
        Branch 账单 billProc
        Branch 流量 trafficProc
        Branch 余额 balanceProc
        Branch 退出 exitProc

        Step billProc
        Speak "您的本月账单是" + $bill + "元"
        Listen 5
        Branch 返回 welcome
        Branch 退出 exitProc

        Step trafficProc
        Speak "您的本月流量是" + $traffic + "GB"
        Listen 5
        Branch 返回 welcome
        Branch 退出 exitProc

        Step balanceProc
        Speak "您的账户余额是" + $balance + "元"
        Listen 5
        Branch 返回 welcome
        Branch 退出 exitProc

        Step complainProc
        Speak "非常抱歉造成不便，我们将尽快处理您的投诉"
        Listen 5
        Branch 返回 welcome
        Branch 退出 exitProc

        Step exitProc
        Speak "感谢使用，再见"
        Exit
        """
        
        if stub.upload_script(script_content):
            # 初始化变量
            initial_vars = {
                "name": {"value": "李女士", "type": "text"},
                "balance": {"value": 5000, "type": "number"},
                "bill": {"value": 300, "type": "number"},
                "traffic": {"value": 20, "type": "number"}
            }
            stub.initialize_variables(initial_vars)
            
            # 模拟用户交互
            user_inputs = ["查询", "账单", "返回", "投诉", "退出"]
            interactions = stub.simulate_interaction(user_inputs)
            
            print("\n交互详情:")
            for interaction in interactions:
                print(f"用户输入: {interaction['user_input']}")
                print(f"系统响应: {interaction['response']}")

    @staticmethod
    def scenario_3_error_handling():
        """
        错误处理场景：处理无效输入
        """
        print("\n=== 场景3：错误处理流程 ===")
        stub = DSLFrontendStub()
        
        # 上传带有错误处理的DSL脚本
        script_content = """
        Step welcome
        Speak $name + "您好，请输入正确的指令"
        Listen 10
        Branch 确认 confirmProc
        Default defaultProc

        Step confirmProc
        Speak "您确认继续吗?"
        Listen 10
        Branch 是 successProc
        Branch 否 exitProc
        Default defaultProc

        Step defaultProc
        Speak "抱歉，我没有理解您的指令"
        Listen 5
        Branch 重试 welcome
        Branch 退出 exitProc

        Step successProc
        Speak "操作成功!"
        Exit

        Step exitProc
        Speak "感谢使用，再见"
        Exit
        """
        
        if stub.upload_script(script_content):
            # 初始化变量
            initial_vars = {
                "name": {"value": "王经理", "type": "text"}
            }
            stub.initialize_variables(initial_vars)
            
            # 模拟用户交互
            user_inputs = ["无效指令", "确认", "不确定", "是"]
            interactions = stub.simulate_interaction(user_inputs)
            
            print("\n交互详情:")
            for interaction in interactions:
                print(f"用户输入: {interaction['user_input']}")
                print(f"系统响应: {interaction['response']}")

def main():
    # 运行不同的交互场景
    DSLFrontendStubDemo.scenario_1_basic_interaction()
    DSLFrontendStubDemo.scenario_2_complex_interaction()
    DSLFrontendStubDemo.scenario_3_error_handling()

if __name__ == '__main__':
    main()