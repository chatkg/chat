# -*- coding: utf-8 -*-
"""Chat client. 聊天客户端。

Available functions:
- question_pack: Package the question as the JSON format specified by the server.
将问题打包为服务器指定的json格式。
- config_pack: Package the config info as the JSON format specified by the server.
将配置信息打包为服务器指定的json格式。
- match：Match the answers from the semantic knowledge database.
从语义知识数据库搜索答案。
- config：Configure the semantic knowledge database.
配置语义知识数据库。
"""

import json
import socket
# from .mytools import time_me
from .config import getConfig

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(( getConfig("nluserver", "host"), int(getConfig("nluserver", "port")) ))

def question_pack(info="", userid="A0001"):
    """Package the question as the JSON format specified by the server.
    将问题打包为服务器指定的json格式。

    Args:
        info: User question. 用户的聊天或提问。
            Defaults to "".
        userid: User id. 用户唯一标识。
            Defaults to "userid".

    Returns:
        Packaged JSON format data. 打包好的json格式数据。
    """
    data = {
        "userid": userid, # 用户唯一标识
        "key": "yourkey", # API密钥
        "ask_type": "txt", # 问题的类型(txt, img, audio, video)
        "ask_content": info, # 问题内容
        "state": "robotstate" # 机器人状态
        }
    return json.dumps(data)

def config_pack(info="", userid="A0001"):
    """Package the config info as the JSON format specified by the server.
    将配置信息打包为服务器指定的json格式。

    Args:
        info: User config info. 用户配置信息。
            Defaults to "".
        userid: User id. 用户唯一标识。
            Defaults to "userid".

    Returns:
        Packaged JSON format data. 打包好的json格式数据。
    """
    data = {
        "userid": userid, # 用户唯一标识
        "key": "yourkey", # API密钥
        "config_type": "subgraph", # 配置的类型
        "config_content": info, # 配置内容
        "state": "robotstate" # 机器人状态
        }
    return json.dumps(data)

def match(question="question", userid="A0001"):
    """Match the answers from the semantic knowledge database.
    从语义知识数据库搜索答案。

    Args:
        question: User question. 用户问题。
            Defaults to "question".
        userid: User id. 用户唯一标识。
            Defaults to "userid".

    Returns:
        Packaged JSON format data of answer. 打包好的答案json格式数据。
    """
    send = question_pack(question, userid)
    mysock.sendall(send.encode("UTF-8"))
    received = mysock.recv(4096) # 2048->4096(2018-1-5 添加了 xml 后扩充)
    received = received.decode("UTF-8")
    return received

def config(info="", userid="A0001"):
    """Configure the semantic knowledge database.
    配置语义知识数据库。

    Args:
        info: User config info. 用户配置信息，以空格分隔的知识库名称字符串。
            Defaults to "". 返回可配置选项信息。
        userid: User id. 用户唯一标识。
            Defaults to "userid".

    Returns:
        Packaged JSON format data of config result. 打包好的配置结果json格式数据。
    """
    send = config_pack(info, userid)
    mysock.sendall(send.encode("UTF-8"))
    received = mysock.recv(4096) # 2048->4096(2018-1-5 添加了 xml 后扩充)
    received = received.decode("UTF-8")
    return received

def start():
    """Start Client.
    启动客户端。
    """
    while True:
        question = input("\n>>question=")
        # userid = input(">>userid=")
        # if not userid:
            # userid = "A0001"
        if question == "config":
            result = config(info="", userid="A0001")
        else:
            result = match(question=question, userid="A0001")
        # print(json.loads(result))
        print(json.loads(result)['content'])

# @time_me()
def batch_test(filename, userid="A0001"):
    """Batch test.
    """
    assert filename is not None, "filename can not be None"
    data = []
    with open("testresult.txt", 'w', encoding="UTF-8") as file:
        with open(filename, 'r', encoding="UTF-8") as testcase:
            for line in testcase:
                if not line:
                    continue
                question = line.rstrip()
                result = json.loads(match(question=question, userid=userid))
                data.append(result)
                for key in ["question", "content", "behavior", "url", "context", "parameter"]:
                    file.write(key + ": " + str(result[key]) + "\n")
                file.write("\n")
    return data
