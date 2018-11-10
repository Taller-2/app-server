from datetime import datetime

import requests
from haversine import haversine

from server.model.account import Account
from server.model.article import Article

URL = 'https://taller2-shared-server.herokuapp.com/'
# URL = 'http://localhost:3000/'


def shipment_cost(article: Article, lat: float, lon: float,
                  payment_method: str):
    account = Account.current()
    now = datetime.now()
    return requests.post(URL + 'shipment-cost', json={
        'antiquity': account.antiquity(),
        'email': account['email'],
        'userScore': account.score(),
        'paymentMethod': payment_method,
        'distance': haversine(
            (lat, lon),
            (article['latitude'], article['longitude'])
        ),
        'latitude': lat,
        'longitude': lon,
        'tripDate': now.strftime('%Y/%m/%d'),
        'tripTime': now.strftime('%H:%M')
    })
