import os

from flask import send_from_directory

from server.index import app


@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('template', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)

