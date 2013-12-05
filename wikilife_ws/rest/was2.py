# coding=utf-8

from wikilife_utils.parsers.date_parser import DateParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless, authenticated
from wikilife_ws.utils.route import Route


class BaseWas2Handler(BaseHandler):

    _stat_srv = None

    def initialize(self):
        super(BaseWas2Handler, self).initialize()
        self._stat_srv = self._service_builder.build_stat_service()


@Route('/4/was')
class GlobalWasHandler(BaseWas2Handler):
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

        report = self._stat_srv.get_stat_by_id(52, **params)
        self.success(report)


@Route('/4/was/user')
class UserWasHandler(BaseWas2Handler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        raw_params = self.get_str_params()
        params = {}
        params["node_id"] = int(raw_params["node_id"])
        params["metric_id"] = int(raw_params["metric_id"])
        params["user_id"] = user_id
        params["from_date"] = DateParser.from_date(raw_params["from"])
        params["to_date"] = DateParser.from_date(raw_params["to"])

        report = self._stat_srv.get_stat_by_id(52, **params)
        self.success(report)


routes = Route.get_routes()