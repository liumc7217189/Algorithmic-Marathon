from flask import Flask,jsonify,request,render_template
import os, importlib
from werkzeug.utils import secure_filename

app = Flask(__name__)

global results, stepResults, curStep, totalStep, stepResultsArray, ac, user
results = []
stepResults = []
curStep = 1
totalStep = 200
stepResultsArray = []
ac = importlib.import_module("algorithm_core")
user = "player1"

@app.route('/')
def hello_world():
    global user,results
    return render_template("init.html",user=user,result=results)

@app.route('/getUserName')
def getUser():
    global user,results
    user = request.values.get("username")
    return render_template("init.html",user=user,result=results)

@app.route('/uploadFile', methods=['POST'])
def uploadCore():
    f = request.files['file']
    print(f)
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    upload_path = os.path.join(basepath, '', secure_filename(f.filename))
    print(upload_path)
    f.save(upload_path)
    global ac,user,results
    ac = importlib.import_module(os.path.splitext(f.filename)[0])
    importlib.reload(ac)
    return render_template("init.html",user=user,result=results)

@app.route('/start', methods=['POST','GET'])
def start():
    global stepResults,curStep
    curStep = 1
    stepResults = []
    return jsonify({})

@app.route('/step', methods=['POST','GET'])
def step():
    global user,ac,stepResults,curStep,totalStep
    stepResults.append(request.json)
    r = {'action':ac.algorithm_main(request.json, user, curStep, totalStep)}
    curStep += 1
    return jsonify(r)

@app.route('/end', methods=['POST','GET'])
def end():
    global results,stepResultsArray,stepResults
    results.append(request.json)
    stepResultsArray.append(stepResults)
    return jsonify({})

@app.route('/detail', methods=['POST','GET'])
def detail():
    global stepResultsArray
    i = int(request.values.get("curID"))
    if len(stepResultsArray) > 0:
        if len(stepResultsArray[i - 1]) > 0:
            return render_template("detail.html", steps=stepResultsArray[i - 1])
        else:
            return "空数据，请检查代码!!!"
    else:
        return "空数据，请检查代码!!!"


if __name__ == '__main__':
    app.run()
