# coding=utf-8

from wikilife_utils.parsers.date_parser import DateParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless


class AggregationGlobalStatsHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["metric_id"] = int(raw_params["metric_id"])
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        r = stat_srv.get_stat_by_id(100, **params)
        self.success(r)


class ExerciseGlobalStatsHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        r = stat_srv.get_stat_by_id(100, **params)
        self.success(r)


class SocialGlobalStatsHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        r = stat_srv.get_stat_by_id(103)
        self.success(r)


class EducationGlobalStatsHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        r = stat_srv.get_stat_by_id(101)
        self.success(r)


class WorkGlobalStatsHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        r = stat_srv.get_stat_by_id(102)
        self.success(r)


class HealthGlobalComplaintsRankingHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        r = stat_srv.get_stat_by_id(105)
        self.success(r)


class HealthGlobalConditionsRankingHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        stat_srv = self._services["stat"]
        r = stat_srv.get_stat_by_id(107)
        self.success(r)
