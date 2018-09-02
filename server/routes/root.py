from flask import send_from_directory

from server.index import app


@app.route('/')
def index():
    """ static files serve """
    return send_from_directory('template', 'index.html')
