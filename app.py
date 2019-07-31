from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

from models.classifier import Classifier

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/read')
def read():
    return render_template("read.html")

@app.route('/cut', methods=['POST'])
def cut():
    text = request.json
    return jsonify(Classifier().cut_from_text(text['data']))


if __name__ == '__main__':
    app.run()
