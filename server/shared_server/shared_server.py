from datetime import datetime

import requests
from haversine import haversine

from server.model.account import Account
from server.model.article import Article
from server.model.purchase import Purchase
from server.utils import get_shared_server_auth_header

URL = 'https://taller2-shared-server.herokuapp.com/'
# URL = 'http://localhost:3000/'


def request(method, url, **kwargs):
    return requests.request(
        method,
        f'{URL}{url}',
        headers=get_shared_server_auth_header(),
        **kwargs
    )


def shipment_cost(article: Article, lat: float, lon: float,
                  payment_method: str):
    account = Account.current()
    now = datetime.now()
    return request('POST', 'shipment-cost', json={
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


def create_payment(amount: float, payment_method: str, purchase: Purchase):
    return request('POST', 'payments', json={
        'amount': amount,
        'paymentMethod': payment_method,
        'purchaseID': purchase.get_id()
    })


def create_shipment(transaction_id: int, address: str):
    return request('POST', 'shipments', json={
        'transactionId': transaction_id,
        'address': address
    })
