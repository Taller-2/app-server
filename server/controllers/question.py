from server.model.account import Account
from server.model.article import Article
from server.model.question import Question


class QuestionController:
    OWNER = 'owner'

    def __init__(self, *_, **kwargs):
        self.args = kwargs

        self.owner = self.args.pop(self.OWNER, [None])[0]

    def get_questions(self):
        if self.owner:
            return self.get_by_owner()

        result = []
        for question in Question.get_many(**self.args):
            question = question.to_json()
            question['article'] = \
                Article.get_one(question.pop('article_id')).to_json()
            result.append(question)

        return result

    def get_by_owner(self):
        account = Account.get_one(self.owner)
        article_ids = [a.get_id()
                       for a in Article.get_many(user=account['user_id'])]
        questions = []
        for article_id in article_ids:
            questions.extend(
                Question.get_many(article_id=article_id)
            )
        return questions
