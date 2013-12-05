# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.route import Route


class BaseLogsHandler(BaseHandler):

    _log_srv = None

    def initialize(self):
        super(BaseLogsHandler, self).initialize()
        self._log_srv = self._service_builder.build_log_service()
        self._gs_srv = self._service_builder.build_gs_service()

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


@Route("/4/logs")
class LogCollectionHandler(BaseLogsHandler):
    """
    """

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
        logs = self.get_logs(self.request.body, user_id)
        inserted_ids = self._log_srv.add_logs(logs)
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
        logs = self.get_logs(self.request.body, user_id)
        inserted_ids = self._log_srv.edit_logs(logs)
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
        logs = self.get_logs(self.request.body, user_id)
        self._log_srv.delete_logs(logs)
        self.success()


@Route("/4/logs/latest")
class LatestFinalLogsHandler(BaseLogsHandler):
    """
    """

    @catch_exceptions
    def get(self):
        """
        Returns the lastest `amount` logs.
        Does not include any user-sensitive inforomation.

        :param amount: Amount of logs to return. Defaults to 20.

        """
        amount = self.get_argument("amount", 20)
        latest_logs = self._gs_srv.get_latest_logs(amount)
        self.success(latest_logs)


routes = Route.get_routes()
