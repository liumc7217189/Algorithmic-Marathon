from flask import Flask,jsonify,request
import random

app = Flask(__name__)


@app.route('/')
def hello_world():
    print("test1")
    return jsonify({})

@app.route('/start', methods=['POST','GET'])
def start():
    print("test1 start")
    return jsonify({})

stepFlag = ['U','D','L','R','S']
@app.route('/step', methods=['POST','GET'])
def step():
    print(request.json)
    i = random.randint(0,4)
    s1 = {'action': stepFlag[i]}
    return jsonify(s1)

@app.route('/end', methods=['POST','GET'])
def end():
    print("test1 stop!!")
    return jsonify({})

if __name__ == '__main__':
    app.run()
