from flask import Flask, request
from framework.webdriver import WebDriver
from framework.util.response import Response
from framework.util.constant import *
from framework.util.config import FlaskConfig
import os, signal

app = Flask(__name__)
app.webdriver = WebDriver()

@app.route('/')
def index():
    """Flask app home page
    
    Returns:
        test response
    """
    return Response(TEST).props

@app.route('/application')
def application():
    """Endpoint for the application webpage to get data to update page with"""
    if app.webdriver.isConfigured:
        url, count, maxCount = app.webdriver.device.url, app.webdriver.currentCount, app.webdriver.maxCount
        match count:
            case 0:
                status = STATUS_READY
            case _ if count > 0:
                status = STATUS_STARTED
            case _:
                status = STATUS_ERROR
    else:
        status, url, count, maxCount = STATUS_IDLE, DRIVER_NOT_CONFIGURED, 0, 0
    values = {'status': status, 'url': url, 'count': count, 'max': maxCount}
    return Response('Application UI Update', **values).props

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the application -- kills the webdriver and flask app
    
    Returns:
        JSON response
    """
    if app.webdriver:
        app.webdriver.shutdown()
    os.kill(os.getpid(), signal.SIGINT)
    return Response(SHUT_DOWN).props
    
@app.route('/webdriver/configure', methods=['POST'])
def configureWebDriver():
    """Configure the webdriver if it has not already been configured
    
    Returns:
        JSON response
    """
    message = None
    if app.webdriver.isConfigured:
        message = DRIVER_ALREADY_CONFIGURED
    else:
        isValid, error = processRequest(request)
        if isValid:
            app.webdriver.configure(**request.json)
            message = DRIVER_CONFIGURED
        else:
            message = error
    return WebDriverResponse(message, False)

@app.route('/webdriver/clear', methods=['POST'])
def clearWebDriver():
    """Clear the webdriver from the flask app if it has been configured
    
    Returns:
        JSON response
    """
    message = None
    if app.webdriver.isConfigured:
        app.webdriver.shutdown()
        message = DRIVER_CLEARED
    return WebDriverResponse(message, False)

@app.route('/webdriver/status', methods=['GET'])
def getWebDriverStatus():
    """Get the current status of the webdriver
    
    Returns:
        JSON response
    """
    return WebDriverResponse(DRIVER_CONFIGURED, False)

@app.route('/webdriver/url', methods=['GET'])
def getWebDriverUrl():
    """Get the url configured on the webdriver if it is configured
    
    Returns:
        JSON response
    """
    message = app.webdriver.device.url if app.webdriver.isConfigured else None
    return WebDriverResponse(message, False)

@app.route('/webdriver/metrics', methods=['GET'])
def getMetrics():
    """Get the current metrics from the webdriver 
    
    Returns:
        JSON response
    """
    return WebDriverResponse(DRIVER_METRICS)

@app.route('/webdriver/add-session', methods=['POST'])
def addSession():
    """Add a session from the webdriver if it eis configured
    
    Returns:
        JSON response
    """
    message = None
    if app.webdriver.isConfigured:
        app.webdriver.addSession()
        message = SESSION_ADDED
    return WebDriverResponse(message)

@app.route('/webdriver/remove-session', methods=['POST'])
def removeSession():
    """Remove a session from the webdriver if it eis configured
    
    Returns:
        JSON response
    """
    message = None
    if app.webdriver.isConfigured:
        if app.webdriver.currentCount > 1:
            app.webdriver.removeSession()
            message = SESSION_REMOVED
        else:
            message = SESSION_LOWER_LIMIT
    return WebDriverResponse(message)



def processRequest(request):
    """Process the request json to ensure it has the correct format
    
    Args:
        request: incoming request from flask endpoint (/webdriver/configure)
    Returns:
        isValid, error
    """
    try:
        data = request.json
        isValid = (isinstance(data, dict)) and ('url' in data.keys())
        error = None if 'url' in data.keys() else REQUEST_ERROR_FORMAT
    except Exception as e:
        isValid = False
        error = str(e)
    return isValid, error

def WebDriverResponse(message, includeSessions=True):
    """ """
    args = {
        'message': message if app.webdriver.isConfigured else DRIVER_NOT_CONFIGURED
    }
    if includeSessions:
        args['sessions'] = app.webdriver.count
    return Response(**args).props

if __name__ == "__main__":
    app.run(**FlaskConfig())