from flask import Flask, request, render_template
import os, signal, datetime

app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return {'timestamp': datetime.datetime.now()}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    return render_template('metrics.html')

def startApplication():
    return app.run(host='0.0.0.0', port=5000, debug=True)