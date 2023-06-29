from flask import Flask, request, render_template
from framework.webdriver import WebDriver
from framework.response import Response
from framework.util.constant import *
from framework.util import config
import os, signal

app = Flask(__name__)
app.webdriver = None

@app.route('/test')
def test():
    """Test response endpoint"""
    return Response(TEST).props

@app.route('/')
def index():
    """ """
    return render_template('index.html')

@app.route('/metrics', methods=['GET'])
def getMetrics():
    """ """
    if app.webdriver:
        metrics = {
            'count': app.webdriver.currentCount
            , 'max': app.webdriver.maxCount
        }
        response = Response(message=DRIVER_METRICS, **metrics)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/shutdown')
def shutdown():
    """ """
    app.webdriver.shutdown()
    os.kill(os.getpid(), signal.SIGINT)
    return Response(SHUT_DOWN).props
    
@app.route('/webdriver/configure/', methods=['POST'])
def configureWebDriver():
    """ """
    if app.webdriver:
        response = Response(DRIVER_ALREADY_CONFIGURED)
    else:
        isValid, error = processRequest(request)
        if isValid:
            #app.webdriver = WebDriver(**request.json)
            response = Response(DRIVER_CONFIGURED)
        else:
            response = Response(DRIVER_CONFIGURE_ERROR, error=error)
    return response.props

@app.route('/webdriver/clear', methods=['POST'])
def clearWebDriver():
    """ """
    if app.webdriver:
        app.webdriver.shutdown()
        del app.webdriver
        app.webdriver = None
        response = Response(DRIVER_CLEARED)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/status', methods=['GET'])
def getWebDriverStatus():
    """ """
    response = Response(DRIVER_CONFIGURED if app.webdriver else DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/add-session', methods=['POST'])
def addSession():
    """ """
    if app.webdriver:
        app.webdriver.add_session()
        response = Response(SESSION_ADDED)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/remove-session', methods=['POST'])
def removeSession():
    """ """
    if app.webdriver:
        app.webdriver.remove_session()
        response = Response(SESSION_REMOVED)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

def processRequest(request):
    """Process the request json to ensure it has the correct format"""
    try:
        data = request.json
        isValid = (isinstance(data, dict)) and ('url' in data.keys())
        if isinstance(data, dict):
            if ['url'] == data.keys():
                error = None
            else:
                error = REQUEST_ERROR_FORMAT
        else:
            error = REQUEST_ERROR_TYPE
    except Exception as e:
        isValid = False
        error = str(e)
    return isValid, error

if __name__ == "__main__":
    app.run(**config.get('app'))