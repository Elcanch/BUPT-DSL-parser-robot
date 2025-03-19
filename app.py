'''
Author: Elichen 2954855725@qq.com
Date: 2024-12-12 08:26:47
LastEditors: Elichen 2954855725@qq.com
LastEditTime: 2024-12-16 21:38:21
FilePath: \code\py\MyDsl\app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import queue
import sys
import io
from flask import Flask, request, jsonify
import Interpreter_fixed as Interpreter
import Parser
from flask_cors import CORS
import threading
app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/dataInit', methods=['POST'])
def dataInit():
    """初始化数据。"""
    init_data = interpreter.script.variables
    variables = {}
    for key, value in init_data.items():
        if isinstance(value, str):
            variables[key] = {"value": value, "type": "text"}
        elif isinstance(value, (int, float)):
            variables[key] = {"value": value, "type": "number"}
    print(variables)
    return jsonify({"variables": variables}), 200

@app.route('/initialize', methods=['POST'])
def initialize():
    """初始化 DSL 系统变量。"""
    data = request.json
    print(data)
    print("Received data:", data)  # 打印接收到的表单数据
    try:
        variables = {key: value['value']  for key, value in data.items()}
        print("Processed variables:", variables)  # 打印提取的变量

        for key, value in variables.items():
            interpreter.variables[key] = value
        result = interpreter.execute()
        if interpreter.currentStep.listen:
            timeout = interpreter.currentStep.listen
        return jsonify({
            "result": result,
            "variables": interpreter.variables,
            "timeout": timeout,
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/process', methods=['POST'])
def process():
    """处理用户输入并返回响应。"""
    data = request.json
    user_input = data.get('input', 'silence')
    print(f"Received input: {user_input}")  # 打印接收到的用户输入
    if user_input == '' or user_input is None:
        user_input = "silence"
    try:
        interpreter.setUserInput(user_input)
        is_exit = False
        next_step_id = interpreter.getNextStep(user_input)
        
        print(f"Next step id: {next_step_id}")
        interpreter.currentStep = interpreter.script.steps[next_step_id]
        current_step = interpreter.currentStep

        if current_step.speak:
            response = interpreter.execSpeak(current_step.speak)
        else:
            response = ""
        if current_step.exit:
            is_exit = True
        print(f"Response: {response}")  # 打印返回的响应
        if current_step.listen:
            interpreter.execListen(current_step.listen)
        else:
            current_step.listen = 100
        
        return jsonify({
            "response": response,
            "next_step": interpreter.currentStep.stepID,
            "is_exit": is_exit,
            "timeout": interpreter.currentStep.listen,
        }), 200
    except Exception as e:
        print(f"Error occurred in process route: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload():
    """上传 DSL 脚本文件并解析。"""
    data = request.json
    script_content = data.get('input', '')
    print(f"Received content: {script_content}")  # 打印接收到的文件名
    try:
        global parser
        parser = Parser.parser()  # 初始化 DSL 解析器
        parser.parseText(script_content)   # 解析 DSL 脚本文件
        global interpreter
        interpreter = Interpreter.Interpreter(parser)  # 初始化解释器
        if interpreter.script.success:
            response = "DSL 脚本文件上传成功！"
            return jsonify({"response": response}), 200
        else:
            response = "DSL 脚本文件上传失败！"
            return jsonify({"response": response}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    # 初始化 DSL 解析器和解释器
    parser = None
    interpreter = None
    app.run(debug=True)