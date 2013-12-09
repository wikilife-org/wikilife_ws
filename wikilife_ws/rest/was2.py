# coding=utf-8

from wikilife_utils.parsers.date_parser import DateParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless, authenticated


class GlobalWasHandler(BaseHandler):
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

        report = stat_srv.get_stat_by_id(52, **params)
        self.success(report)


class UserWasHandler(BaseHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        stat_srv = self._services["stat"]
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["metric_id"] = int(raw_params["metric_id"])
        params["user_id"] = user_id
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        report = stat_srv.get_stat_by_id(52, **params)
        self.success(report)
