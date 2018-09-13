from bson.json_util import dumps
from flask import request, Blueprint, Response, jsonify

from firebase_admin import db as firebase
from server.model import crud

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')

USERS = firebase.reference('users')


def validate_token(data):
    if "token" not in data:
        return None, "The token is needed"
    user = USERS.child(data["token"]).get()
    if user is None:
        return user, "the user has not logged in"
    return user, ""


def validate_user_with_article(an_article, user):
    if an_article['id_user'] != user['id']:
        return False, "Sorry, This article belongs to another user"
    return True, ""


@ARTICLES_BP.route('/', methods=['GET', 'POST'])
def article():
    if request.method == 'GET':
        # we are supposed to receives the token of the user who has logged in
        # and wants to get an article
        data = request.args
        user, msg = validate_token(data)
        if user is None:
            return msg
        an_article = crud.get(request.args, 'articles')
        valid, msg = validate_user_with_article(an_article, user)
        if not valid:
            return msg
        return Response(
            response=dumps(an_article),
            status=200,
            mimetype='application/json'
        )

    # POST
    # we are supposed to receives the token of the user who has logged in
    # and wants to post an article and also the article info
    data = request.get_json()
    user, msg = validate_token(data)
    if user is None:
        return msg
    del data["token"]  # remove the token because we di not need it as info
    # to the article
    return crud.post(
        data,
        'articles',
        ('name', 'description', 'available_units', 'price', 'id_user')
    )
