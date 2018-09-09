import flask
from bson.json_util import dumps
from flask import request, Blueprint

from server.libs.mongo import mongo
from server.model import crud

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/', methods=['GET', 'POST'])
def article():
    if request.method == 'GET':
        return flask.Response(
            response=dumps(mongo.db['articles'].find(request.args)),
            status=200,
            mimetype='application/json'
        )
    return crud.post(
        request.get_json(),
        'articles',
        ('name', 'description', 'available_units', 'price')
    )
