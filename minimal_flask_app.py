from flask import Flask

def createApp():
    app = Flask(__name__)
    return app

@app.route('/')
def hello_world():
    return "<p> Hello World 3</p>"
