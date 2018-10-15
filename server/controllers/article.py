from haversine import haversine

from server.model.article import Article


class ArticleController:

    MY_LATITUDE = 'my_lat'
    MY_LONGITUDE = 'my_lon'
    MAX_DISTANCE = 'max_distance'

    PRICE_MIN = 'price_min'
    PRICE_MAX = 'price_max'

    DISTANCE_ARGS = [MY_LATITUDE, MY_LONGITUDE, MAX_DISTANCE]

    def __init__(self, *_, **kwargs):
        self.args = kwargs
        self.lat: float = None
        self.lon: float = None
        self.max_distance: float = None

        self.price_min: float = None
        self.price_max: float = None

        self._validate_args()

    def _validate_args(self):
        for arg in self.args:
            if arg not in self._get_valid_arg_keys():
                msg = f"Argument {arg} invalid for an article query"
                raise ValueError(msg)

        self._init_distance_args()
        self._init_price_args()

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
        return list(Article.schema.keys()) + self.DISTANCE_ARGS + \
            [self.PRICE_MIN, self.PRICE_MAX]

    def get_articles(self):
        if self.price_min or self.price_max:
            articles = self.get_with_price_filters()
        else:
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

    def _init_price_args(self):
        try:
            self.price_min = self._get_price_arg(self.PRICE_MIN)
            self.price_max = self._get_price_arg(self.PRICE_MAX)
        except ValueError:
            price_args = ', '.join([self.PRICE_MAX, self.PRICE_MIN])
            msg = f"Price arguments {price_args} must be numeric"
            raise ValueError(msg)

    def _get_price_arg(self, arg):
        value = self.args.pop(arg, None)
        if value is None:
            return None
        return float(value[0])

    def get_with_price_filters(self):
        query = Article.make_mongo_query(self.args)
        new_queries = []
        if self.price_max:
            new_queries.append({"price": {"$lte": self.price_max}})
        if self.price_min:
            new_queries.append({"price": {"$gte": self.price_min}})

        query["$and"] = query.get("$and", []) + new_queries
        return Article.run_query(query)
