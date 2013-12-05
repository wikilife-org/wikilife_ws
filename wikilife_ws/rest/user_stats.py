# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.route import Route
import datetime


class BaseStatHandler(BaseHandler):

    _stat_srv = None

    def initialize(self):
        super(BaseStatHandler, self).initialize()
        self._stat_srv = self._service_builder.build_stat_service()


@Route('/4/stats/user/health/complaints/mostpopular/500')
class HealthUserComplaintsRankingHandler(BaseStatHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        params = {}
        params["user_id"] = user_id

        r = self._stat_srv.get_stat_by_id(106, **params)
        self.success(r)




'''
class BaseUserStatHandler(BaseHandler):

    _stat_srv = None

    def initialize(self):
        super(BaseUserStatHandler, self).initialize()
        self._stat_srv = self._service_builder.build_stat_service()


@Route("/3/stats/user/log_activity/(?P<loggable_id>[-\w]+)")
class UserLogActivityStatHandler(BaseUserStatHandler):
    """
    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id, loggable_id):
        """
        Returns aggregated stats for a single loggable for a single user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365, 730]

        result = self._stat_srv.readers[str(9)].read_stat(user_id, date, loggable_id, ranges)
        self.success(result, dev_message="Loggable Node by User")


@Route("/3/stats/user/aggregation/(?P<loggable_id>[-\w]+)")
class UserAggregationStatHandler(BaseUserStatHandler):
    """
    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id, loggable_id):
        """
        Returns aggregated stats for a single loggable for a single user.

        Response::

            {
              "status": "OK",
              "message": "Loggable Node Aggregation by User",
              "data": {
                "365": {
                  "count": 71,
                  "297": {
                    "count": 66,
                    "298": {
                      "count": 66,
                      "sum": 3960
                    }
                  },
                  "241560": {
                    "count": 1,
                    "241561": {
                      "count": 1,
                      "sum": 1
                    }
                  },
                  "299": {
                    "count": 4,
                    "300": {
                      "count": 4,
                      "sum": 4
                    }
                  }
                },
                "30": {
                  "count": 19,
                  "297": {
                    "count": 14,
                    "298": {
                      "count": 14,
                      "sum": 840
                    }
                  },
                  "241560": {
                    "count": 1,
                    "241561": {
                      "count": 1,
                      "sum": 1
                    }
                  },
                  "299": {
                    "count": 4,
                    "300": {
                      "count": 4,
                      "sum": 4
                    }
                  }
                },
                "7": {
                  "count": 7,
                  "297": {
                    "count": 3,
                    "298": {
                      "count": 3,
                      "sum": 180
                    }
                  },
                  "241560": {
                    "count": 1,
                    "241561": {
                      "count": 1,
                      "sum": 1
                    }
                  },
                  "299": {
                    "count": 3,
                    "300": {
                      "count": 3,
                      "sum": 3
                    }
                  }
                }
              }
            }

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 365]

        result = self._stat_srv.readers[str(17)].read_stat(user_id, date, loggable_id, ranges)
        self.success(result, dev_message="Loggable Node Aggregation by User")


@Route("/3/stats/user/food/top_5")
class TopFiveFoodStatsHandler(BaseUserStatHandler):
    """
        "status": "OK",
            "message": "Top Five Food",
            "data": {
                "90": [],
                "180": [
                    {
                        "count": 33,
                        "position": 1,
                        "node_id": 222886,
                        "calories": 990,
                        "title": "Espresso with Sugar"
                    },
                    {
                        "count": 29,
                        "position": 2,
                        "node_id": 195742,
                        "calories": 474,
                        "title": "Yerba Mate Unsweetened Mate - Guayaki"
                    },
                    {
                        "count": 16,
                        "position": 3,
                        "node_id": 189058,
                        "calories": 4255,
                        "title": "Fruit Juice"
                    },
                    {
                        "count": 15,
                        "position": 4,
                        "node_id": 50992,
                        "calories": 1029.1999999999998,
                        "title": "Blueberries"
                    },
                    {
                        "count": 15,
                        "position": 5,
                        "node_id": 400823,
                        "calories": 1695,
                        "title": "Green Salad "
                    }
                ],
                "365": [
                    {
                        "count": 96,
                        "position": 1,
                        "node_id": 195742,
                        "calories": 1605,
                        "title": "Yerba Mate Unsweetened Mate - Guayaki"
                    },
                    {
                        "count": 69,
                        "position": 2,
                        "node_id": 180538,
                        "calories": 7729.2,
                        "title": "Green Salad - Mimis Cafe"
                    },
                    {
                        "count": 60,
                        "position": 3,
                        "node_id": 222886,
                        "calories": 1800,
                        "title": "Espresso with Sugar"
                    },
                    {
                        "count": 43,
                        "position": 4,
                        "node_id": 189058,
                        "calories": 10511,
                        "title": "Fruit Juice"
                    },
                    {
                        "count": 39,
                        "position": 5,
                        "node_id": 153676,
                        "calories": 41,
                        "title": "Espresso Coffee"
                    }
                ],
                "30": [ ],
                "7": [ ]
            }

        }
    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id):

        """
        Returns top five food for a user.

        Response::



        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365, 730]

        result = self._stat_srv.readers[str(2)].read_stat(user_id, date, ranges)
        self.success(result, dev_message="Top Five Food")


@Route("/3/stats/user/food/nutrients_distribution")
class NutrientsDistributionStatsHandler(BaseUserStatHandler):
    """
        {

            "status": "OK",
            "message": "Nutrients Distribution",
            "data": {
                "90": [
                    {
                        "protein": 248.068,
                        "fiber": 49.78,
                        "carbs": 606.964,
                        "fat": 278.368
                    }
                ],
                "180": [
                    {
                        "protein": 1939.048,
                        "fiber": 700.645,
                        "carbs": 7773.423,
                        "fat": 2019.442
                    }
                ],
                "365": [
                    {
                        "protein": 5700.191,
                        "fiber": 2298.455,
                        "carbs": 22569.223,
                        "fat": 6874.187
                    }
                ],
                "30": [ ],
                "7": [ ]
            }

        }
    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns nutrients distribution for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365]

        result = self._stat_srv.readers[str(3)].read_stat(user_id, date, ranges)
        self.success(result, dev_message="Nutrients Distribution")


@Route("/3/stats/user/food/calories_by_day")
class CaloriesByDayStatsHandler(BaseUserStatHandler):
    """

    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns nutrients distribution for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365]

        result = self._stat_srv.readers[str(7)].read_stat(user_id, date, ranges)
        self.success(result, dev_message="Calories By Day")


@Route("/3/stats/user/food/avg_calories_by_time_range")
class AvgCaloriesbyTimeRangeStatsHandler(BaseUserStatHandler):
    """

    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns nutrients distribution for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365]

        result = self._stat_srv.readers[str(4)].read_stat(user_id, date, ranges)
        self.success(result, dev_message="Avg Calories by Time range")


@Route('/3/stats/user/aggregation')
class ExportGetRequestHandler(BaseUserStatHandler):
    """
    """

    @authenticated    
    @catch_exceptions
    def get(self, user_id, **kwargs):
        params = self.get_params()

        if "from_date" in params:
            from_date = datetime.datetime.strptime(params["from_date"], "%Y%m%d").date()
        else:
            from_date = datetime.date.today()

        if "days_count" in params:
            days_count = int(params["days_count"])
        else:
            days_count = 30

        result = self._stat_srv.readers[str(1)].read_stat(user_id, from_date, days_count)
        self.success(result, dev_message="Loggable Node Aggregation by User")


@Route('/3/stats/user/water/distribution')
class WaterDistributionRequestHandler(BaseUserStatHandler):
    """
    """
    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns water distribution for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        result = self._stat_srv.readers[str(14)].read_stat(user_id, date)
        self.success(result)
            

@Route('/3/stats/user/water/average')
class WaterAverageRequestHandler(BaseUserStatHandler):
    """
    """
    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns water avg for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365]

        result = self._stat_srv.readers[str(6)].read_stat(user_id, date, ranges)
        self.success(result)


@Route('/3/stats/user/exercise/list')
class ExerciseListRequestHandler(BaseUserStatHandler):
    """
    """
    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns exercise list for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        result = self._stat_srv.readers[str(7)].read_stat(user_id, date)
        self.success(result)


@Route('/3/stats/user/exercise/distribution/(?P<node_id>[-\w]+)')
class ExerciseDistributionRequestHandler(BaseUserStatHandler):
    """
    """
    def get(self, node_id, user_id):
        """
        Returns exercise list for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        result = self._stat_srv.readers[str(8)].read_stat(user_id, date, node_id)
        self.success(result)


@Route('/3/stats/user/sleep/distribution')
class SleepDistributionRequestHandler(BaseUserStatHandler):
    """
    """
    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns sleep distribution for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        result = self._stat_srv.readers[str(22)].read_stat(user_id, date)
        self.success(result)


@Route('/3/stats/user/sleep')
class SleepRequestHandler(BaseUserStatHandler):
    """
    """
    @authenticated    
    @catch_exceptions
    def get(self, user_id):
        """
        Returns sleep stats for a user.

        """

        params = self.get_params()
        if "date" in params:
            date = datetime.datetime.strptime(params["date"], "%Y%m%d").date()
        else:
            date = datetime.date.today()

        if "ranges" in params:
            ranges = eval(params["ranges"])
        else:
            ranges = [7, 30, 90, 180, 365]

        result = self._stat_srv.readers[str(21)].read_stat(user_id, date, ranges)
        self.success(result)
'''

routes = Route.get_routes()