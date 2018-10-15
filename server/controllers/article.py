from haversine import haversine

from server.model.article import Article


class ArticleController:

    MY_LATITUDE = 'my_lat'
    MY_LONGITUDE = 'my_lon'
    MAX_DISTANCE = 'max_distance'

    DISTANCE_ARGS = [MY_LATITUDE, MY_LONGITUDE, MAX_DISTANCE]

    def __init__(self, *_, **kwargs):
        self.args = kwargs
        self.lat: float = None
        self.lon: float = None
        self.max_distance: float = None
        self._validate_args()

    def _validate_args(self):
        for arg in self.args:
            if arg not in self._get_valid_arg_keys():
                raise ValueError(f"Argument {arg} invalid for an Article query")

        self._init_distance_args()

    def _init_distance_args(self):
        if not any([x in self.args for x in self.DISTANCE_ARGS]):
            return

        try:
            self.lat = float(self.args.pop(self.MY_LATITUDE)[0])
            self.lon = float(self.args.pop(self.MY_LONGITUDE)[0])
            self.max_distance = float(self.args.pop(self.MAX_DISTANCE)[0])
        except KeyError:
            msg = f"All of {', '.join(self.DISTANCE_ARGS)} " \
                  f"must be specified for a distance filter"
            raise ValueError(msg)
        except ValueError:
            msg = f"Distance arguments {', '.join(self.DISTANCE_ARGS)}" \
                  f"must be numeric"
            raise ValueError(msg)

    def _get_valid_arg_keys(self) -> list:
        return list(Article.schema.keys()) + self.DISTANCE_ARGS

    def get_articles(self):
        articles = Article.get_many(**self.args)

        if not self.max_distance:
            return articles

        filtered_articles = self._filter_by_distance(articles)
        return filtered_articles

    def _filter_by_distance(self, articles: list) -> list:
        filtered_articles = []
        for article in articles:
            source = (self.lat, self.lon)
            dest = (article['latitude'], article['longitude'])
            distance = haversine(source, dest)

            if distance <= self.max_distance:
                filtered_articles.append(article)
        return filtered_articles
