# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated


class LogsHandler(BaseHandler):
    """
    """

    def add_log_source(self, logs, headers):
        source = self.get_source(headers)

        for log in logs:
            if not "source" in log:
                log["source"] = source

    def get_logs(self, request_body, user_id):
        logs = JSONParser.to_collection(self.request.body)

        for log in logs:
            log["userId"] = user_id

        self.add_log_source(logs, self.request.headers)
        
        return logs

    @authenticated
    @catch_exceptions
    def post(self, user_id):
        """
        Submits one or more `Log`_ objects.

        Request::
     
            [
                "<Log object>" 
            ]

        Returns a list with the ids of the newly created log entries.
        """
        log_srv = self._services["log"]
        logs = self.get_logs(self.request.body, user_id)
        inserted_ids = log_srv.add_logs(logs)
        self.success(inserted_ids)

    @authenticated
    @catch_exceptions
    def put(self, user_id):
        """
        Edit one or more `Log`_ objects.

        Request::

            [
                "<Log object>" 
            ]

        Returns a list with the ids of the newly created log entries.
        """
        log_srv = self._services["log"]
        logs = self.get_logs(self.request.body, user_id)
        inserted_ids = log_srv.edit_logs(logs)
        self.success(inserted_ids)

    @authenticated
    @catch_exceptions
    def delete(self, user_id):
        """
        Deletes one or more `Log`_ objects.

        Request::

            [
                "<Log object>" 
            ]

        """
        log_srv = self._services["log"]
        logs = self.get_logs(self.request.body, user_id)
        log_srv.delete_logs(logs)
        self.success()


class LatestFinalLogsHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self):
        """
        Returns the lastest `amount` logs.
        Does not include any user-sensitive inforomation.

        :param amount: Amount of logs to return. Defaults to 20.

        """
        gs_srv = self._services["gs"]
        amount = self.get_argument("amount", 20)
        latest_logs = gs_srv.get_latest_logs(amount)
        self.success(latest_logs)
