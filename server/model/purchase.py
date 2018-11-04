from server.model.account import Account
from server.model.article import Article
from server.model.base import Model


class Purchase(Model):
    db_name = 'purchases'

    schema = {
        'user_id': str,
        'article_id': str,
        'units': int,
    }

    @classmethod
    def get_for_user(cls, user: Account):
        user_id = user.get_id()
        purchases = cls.get_many(user_id=user_id)
        result = []
        for purchase in purchases:
            purchase = purchase.to_json()
            purchase['article'] = Article.get_one(  # N database calls, i know
                str(purchase.pop('article_id'))
            ).to_json()
            result.append(purchase)
        return result
