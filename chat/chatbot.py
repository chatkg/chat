from flask import Flask, render_template, request, jsonify
import os
from .client import match

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():

    # kernel now ready for use
    while True:
        if message == "quit":
            exit()
        elif message == "save":
            kernel.saveBrain("bot_brain.brn")
        else:
            bot_response = match(question = message)
            # print bot_response
            return jsonify({'status':'OK','answer':json.loads(result)['content']})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
