# coding=utf-8

from wikilife_utils.parsers.date_parser import DateParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless
from wikilife_ws.utils.route import Route


class BaseStatHandler(BaseHandler):

    _stat_srv = None

    def initialize(self):
        super(BaseStatHandler, self).initialize()
        self._stat_srv = self._service_builder.build_stat_service()


@Route('/4/stats/global/aggregation/')
class AggregationGlobalStatsHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["metric_id"] = int(raw_params["metric_id"])
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        r = self._stat_srv.get_stat_by_id(100, **params)
        self.success(r)


@Route('/4/stats/global/exercise/times_per_week/avg')
class ExerciseGlobalStatsHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        r = self._stat_srv.get_stat_by_id(100, **params)
        self.success(r)


@Route('/4/stats/global/social/')
class SocialGlobalStatsHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        r = self._stat_srv.get_stat_by_id(103)
        self.success(r)


@Route('/4/stats/global/education/level/')
class EducationGlobalStatsHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        r = self._stat_srv.get_stat_by_id(101)
        self.success(r)


@Route('/4/stats/global/work/experience/')
class WorkGlobalStatsHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        r = self._stat_srv.get_stat_by_id(102)
        self.success(r)


@Route('/4/stats/global/health/complaints/mostpopular/500')
class HealthGlobalComplaintsRankingHandler(BaseStatHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        r = self._stat_srv.get_stat_by_id(105)
        self.success(r)


routes = Route.get_routes()