from flask import Flask, render_template, request, jsonify
import os,sys
sys.path.append("/data/app/chat/")
from chat.client import match

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = request.form['messageText'].encode('utf-8').strip()
    # kernel now ready for use
    while True:
        if message == "quit":
            exit()
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            bot_response = match(question = message)
            # print bot_response
            return jsonify({'status':'OK','answer':json.loads(bot_response)['content']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
