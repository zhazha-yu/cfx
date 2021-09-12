from flask import Flask,render_template,request,redirect,url_for
import json
import os
from werkzeug.utils import secure_filename
from upload import *
import time

time.sleep(1)

app = Flask(__name__)

def read(): 
    with open('./save.json', encoding='utf8')as f1:
        data1 = json.load(f1)

    with open('./cloud.json', encoding='utf8')as f2:
        data2 = json.load(f2)
    return data1,data2

data1,data2=read()

@app.route('/',methods=['GET', 'POST'])
def index():
    data1, data2 = read()
    if request.method == 'POST':
        input_= request.values['input']
        if input in data1:
            result = data1[input_]
        else:
            result = []
        return render_template('search.html',input=input,result=result)
    return render_template('index.html', data1=data1)

@app.route('/cloud',methods=['GET', 'POST'])
def cloud():
    if request.method == 'POST':
        input = request.values['input']
        if input in data2:
            result = data2[input]
        else:
            result = []
        return render_template('search.html',input=input,result=result)
    return render_template('cloud.html', data2=data2)

@app.route('/upload',methods=['GET', 'POST'])
def upload_top():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'exfile', secure_filename(f.filename))
        f.save(upload_path)
        return redirect('success')
    return render_template('upload.html')

@app.route('/state',methods=['GET', 'POST'])
def state():
    if request.method == 'POST':
        data1, data2 = read()
        os.system('python3 upload.py')
        return redirect('success2')
    return render_template('state.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/success2')
def success2():
    return render_template('success2.html')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=1)