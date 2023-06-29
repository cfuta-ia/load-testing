from flask import Flask, request, render_template
from framework.device.device import Device
from framework.webdriver.webdriver import WebDriver
import os, signal, datetime, yaml

app = Flask(__name__)
app.webdriver = WebDriver()

@app.route('/test', methods=['GET', 'POST'])
def test():
    return {'timestamp': datetime.datetime.now()}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def metrics():
    return render_template('status.html')
    
@app.route('/webdriver/set/<file>')
def setWebdriver(file=None):
    device = Device(file)
    app.webdriver.startup(device)
    return f'Webdriver has been set to: {device.name}'

@app.route('/webdriver/add-session')
def addSession():
    """ """
    pass

@app.route('/webdriver/remove-session')
def removeSession():
    """ """
    pass

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ """
    app.webdriver.shutdown()
    os.kill(os.getpid(), signal.SIGINT)
    return {'message': 'Shutting down...', 'value': True}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)