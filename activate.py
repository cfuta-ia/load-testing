from framework.app import application

# Start Flask server
if __name__ == '__main__':
    print('Starting application...')
    app = application()
    app.run(host='0.0.0.0', port=5000, debug=True)