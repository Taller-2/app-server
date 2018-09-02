from flask import send_from_directory

from server.index import app


@app.route('/')
# Esta funcion se llama index2 porque si se llamara
# index rompe el codigo por dos funciones del mismo nombre
def index2():
    """ static files serve """
    return send_from_directory('template', 'index.html')
