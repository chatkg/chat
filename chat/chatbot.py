from flask import Flask, render_template, request, jsonify
import os,sys,json
sys.path.append("/data/app/chat/")
from chat.client import match

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
        bot_response = match(question = message)
        # print bot_response
        return jsonify({'status':'OK','answer':json.loads(bot_response)['content']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
