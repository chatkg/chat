from flask import Flask, render_template, request, jsonify
import os,sys,json,socket
sys.path.append("/data/app/chat/")
from chat.client import match,question_pack
from chat.config import getConfig

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = request.form['messageText'].strip()
    
    if message == "quit":
        exit()
    else:
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect(( getConfig("nluserver", "host"), int(getConfig("nluserver", "port")) ))
        send = question_pack(message, userid = "A0001")
        mysock.sendall(send.encode("UTF-8"))
        received = mysock.recv(4096) # 2048->4096(2018-1-5 添加了 xml 后扩充)
        received = received.decode("UTF-8")

        # print bot_response
        return jsonify({'status':'OK','answer':json.loads(received)['content']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
