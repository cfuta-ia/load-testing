from flask import Flask, request, render_template
from framework.device.device import Device
from framework.webdriver.webdriver import WebDriver
import os, signal, datetime, yaml

def application():
    """ """
    app = Flask(__name__)
    app.webdriver = None

    @app.route('/test', methods=['GET', 'POST'])
    def test():
        return {'timestamp': datetime.datetime.now()}

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/status', methods=['GET'])
    def metrics():
        return render_template('status.html')
        
    @app.route('/webdriver/set/<file>', methods=['POST'])
    def setWebdriver(file=None):
        client = Device(file)
        app.webdriver = WebDriver()
        return None
    
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        """ """
        app.webdriver.shutdown()
        os.kill(os.getpid(), signal.SIGINT)
        return {'message': 'Shutting down...', 'value': True}
    
    return app