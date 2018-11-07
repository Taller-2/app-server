from datetime import datetime

import requests
from haversine import haversine

from server.model.article import Article

URL = 'https://taller2-shared-server.herokuapp.com/'
# URL = 'http://localhost:3000/'


def shipment_cost(article: Article, lat: float, lon: float):
    data = {
        'paymentMethod': 'cash'
    }
    account = article.account()
    if account:
        data['userCharacteristics'] = {
            'antiquity': account.antiquity(),
            'email': account['email'],
        }
    data['userScore'] = account.score()
    data['shippingCharacteristics'] = {
        'distance': haversine(
            (lat, lon),
            (article['latitude'], article['longitude'])
        ),
        'geographicalPosition': {
            'latitude': lat,
            'longitude': lon
        }
    }
    now = datetime.now()
    data['tripDate'] = now.strftime('%Y/%m/%d')
    data['tripTime'] = now.strftime('%H:%M')
    return requests.post(URL + 'shipment-cost', json=data)
