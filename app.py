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
    """Test response endpoint
    
    Returns:
        JSON response
    """
    return Response(TEST).props

@app.route('/')
def index():
    """Flask app home page
    
    Returns:
        'static' html homepage
    """
    return render_template('index.html')

@app.route('/shutdown')
def shutdown():
    """Shutdown the application -- kills the webdriver and flask app
    
    Returns:
        JSON response
    """
    app.webdriver.shutdown()
    os.kill(os.getpid(), signal.SIGINT)
    return Response(SHUT_DOWN).props
    
@app.route('/webdriver/configure/', methods=['POST'])
def configureWebDriver():
    """Configure the webdriver if it has not already been configured
    
    Returns:
        JSON response
    """
    if app.webdriver:
        response = Response(DRIVER_ALREADY_CONFIGURED)
    else:
        isValid, error = processRequest(request)
        if isValid:
            app.webdriver = WebDriver(**request.json)
            response = Response(DRIVER_CONFIGURED)
        else:
            response = Response(DRIVER_CONFIGURE_ERROR, error=error)
    return response.props

@app.route('/webdriver/clear', methods=['POST'])
def clearWebDriver():
    """Clear the webdriver from the flask app if it has been configured
    
    Returns:
        JSON response
    """
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
    """Get the current status of the webdriver
    
    Returns:
        JSON response
    """
    response = Response(DRIVER_CONFIGURED if app.webdriver else DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/metrics', methods=['GET'])
def getMetrics():
    """Get the current metrics from the webdriver 
    
    Returns:
        JSON response
    """
    if app.webdriver:
        metrics = {
            'count': app.webdriver.currentCount
            , 'max': app.webdriver.maxCount
        }
        response = Response(message=DRIVER_METRICS, **metrics)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/add-session', methods=['POST'])
def addSession():
    """Add a session from the webdriver if it eis configured
    
    Returns:
        JSON response
    """
    if app.webdriver:
        app.webdriver.add_session()
        response = Response(SESSION_ADDED)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

@app.route('/webdriver/remove-session', methods=['POST'])
def removeSession():
    """Remove a session from the webdriver if it eis configured
    
    Returns:
        JSON response
    """
    if app.webdriver:
        app.webdriver.remove_session()
        response = Response(SESSION_REMOVED)
    else:
        response = Response(DRIVER_NOT_CONFIGURED)
    return response.props

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