# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated


class HealthUserComplaintsRankingHandler(BaseHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        if user_id == None:
            self.error(error="Unauthorized", user_message="Invalid token", dev_message="Invalid token", status_code=401)
            return

        stat_srv = self._services["stat"]
        params = {}
        params["user_id"] = user_id

        r = stat_srv.get_stat_by_id(105, **params)
        self.success(r)


class HealthUserConditionsRankingHandler(BaseHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        if user_id == None:
            self.error(error="Unauthorized", user_message="Invalid token", dev_message="Invalid token", status_code=401)
            return

        stat_srv = self._services["stat"]
        params = {}
        params["user_id"] = user_id

        r = stat_srv.get_stat_by_id(107, **params)
        self.success(r)


class PsychologicalUserMoodRankingHandler(BaseHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        if user_id == None:
            self.error(error="Unauthorized", user_message="Invalid token", dev_message="Invalid token", status_code=401)
            return

        stat_srv = self._services["stat"]
        params = {}
        params["user_id"] = user_id

        r = stat_srv.get_stat_by_id(109, **params)
        self.success(r)
