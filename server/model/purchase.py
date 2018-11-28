from typing import Optional

from server.model.account import Account
from server.model.article import Article
from server.model.base import Model


class Purchase(Model):
    db_name = 'purchases'

    schema = {
        'user_id': str,
        'article_id': str,
        'units': int,
        'requested_shipment': bool
    }

    @classmethod
    def get_for_user(cls, user: Account):
        user_id = user.get_id()
        purchases = cls.get_many(user_id=user_id)
        return cls.expand(purchases)

    @classmethod
    def expand(cls, purchases):
        result = []
        for purchase in purchases:
            purchase = purchase.to_json()
            purchase['article'] = Article.get_one(  # N database calls, i know
                str(purchase.pop('article_id'))
            ).to_json()
            result.append(purchase)
        return result

    def seller(self) -> Optional[Account]:
        article = Article.get_one(self['article_id'])
        return article.account() if article else None

    def purchaser(self) -> Optional[Account]:
        accounts = Account.get_many(user_id=self['user_id'])
        return accounts[0] if accounts else None

    @classmethod
    def get_by_seller(cls, seller: Account):
        article_ids = [a.get_id() for a in
                       Article.get_many(user=seller['user_id'])]
        if not article_ids:
            return []

        purchases = cls.get_many(article_id=article_ids)
        return cls.expand(purchases)

    def save(self):
        is_new = self.is_new_instance()
        _id = super(Purchase, self).save()
        if not is_new:
            return _id
        seller = self.seller()
        purchaser = self.purchaser()
        if seller:
            seller.register('sale')
        if purchaser:
            purchaser.register('purchase')
        return _id
