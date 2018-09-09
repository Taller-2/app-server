from flask import request, jsonify, Blueprint

from server.model import crud

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/', methods=['GET', 'POST'])
def article():
    if request.method == 'GET':
        return jsonify(crud.get(request.args, 'articles')), 200
    return crud.post(
        request.get_json(),
        'articles',
        ('name', 'description', 'available_units', 'price')
    )
