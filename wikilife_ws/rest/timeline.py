# coding=utf-8

from wikilife_utils.parsers.date_parser import DateParser
from wikilife_utils.parsers.str_parser import StrParser
from wikilife_ws.rest.base_handler import BaseHandler, BaseHandlerV2
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.deprecated import Deprecated


class BaseTimelineHandler(BaseHandler):

    _timeline_srv = None

    def initialize(self):
        super(BaseTimelineHandler, self).initialize()
        self._timeline_srv = self._service_builder.build_timeline_service()

class BaseTimelineHandlerV2(BaseHandlerV2):

    _timeline_srv = None

    def initialize(self):
        super(BaseTimelineHandlerV2, self).initialize()
        self._timeline_srv = self._service_builder.build_timeline_service()


@Deprecated(20130201)
@Route("/2/logs/user_timeline.json")
class UserTimelineHandlerV2(BaseTimelineHandlerV2):
    """
    """

    def get(self):
        """
        Returns the user's timeline.

        Response::

            {
              "status": "OK",
              "message": "Get Stream for User API",
              "data": [
                {
                  "date": "2012-10-26",
                  "_id": {
                    "$oid": "508aedb2e77989792d00001b"
                  },
                  "logs": [
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "RUNNINGnDuration: 60, Intensity: 1",
                      "log_update_datetime_utc": {
                        "$date": 1351282098750
                      },
                      "time": "2012-10-26 17:08:09 -0300",
                      "log_update_datetime": {
                        "$date": 1351292898000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "property_id": 297,
                          "value": "60"
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "property_id": 299,
                          "value": "1"
                        }
                      ],
                      "id": 380904
                    },
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "Running: Duration 60 minutes, Intensity 1 , Distance 1.0 kmnWith? Alone",
                      "log_update_datetime_utc": {
                        "$date": 1351282987710
                      },
                      "time": "2012-10-26 17:14:48 -0300",
                      "log_update_datetime": {
                        "$date": 1351293787000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "value": "60",
                          "property_id": 297
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "value": "1",
                          "property_id": 299
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 241561,
                          "value": "1.0",
                          "property_id": 241560
                        },
                        {
                          "loggable_id": 49,
                          "node_id": 432,
                          "value": "Alone",
                          "property_id": 431
                        }
                      ],
                      "id": 380906
                    },
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "Running: Duration 60 minutes, Intensity 1 ; With? Alone",
                      "log_update_datetime_utc": {
                        "$date": 1351283100286
                      },
                      "time": "2012-10-26 17:24:48 -0300",
                      "log_update_datetime": {
                        "$date": 1351293900000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "property_id": 297,
                          "value": "60"
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "property_id": 299,
                          "value": "1"
                        },
                        {
                          "loggable_id": 49,
                          "node_id": 432,
                          "property_id": 431,
                          "value": "Alone"
                        }
                      ],
                      "id": 380907
                    }
                  ]
                }
              ]
            }

        """
        try:
            user_id = self.get_argument("user_id")
            show_stats = self.get_argument("show_stats", False)

            #categories = StrParser.parse_list(self.get_argument("categories", None))
            categories = StrParser.parse_list(self.get_argument("roots", None))
            from_date = StrParser.parse_date(self.get_argument("from_date", None, True))
            direction = self.get_argument("direction", None)
            if show_stats:
                user_timeline = self._timeline_srv.get_user_timeline_with_daily_stats(user_id, categories, from_date, direction)
            else:
                user_timeline = self._timeline_srv.get_user_timeline(user_id, categories, from_date, direction)

            self.success("Get Stream for User API", user_timeline)

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route("/3/logs/user_timeline")
class UserTimelineHandler(BaseTimelineHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Returns the user's timeline.

        Response::

            {
              "status": "OK",
              "message": "Get Stream for User API",
              "data": [
                {
                  "date": "2012-10-26",
                  "_id": {
                    "$oid": "508aedb2e77989792d00001b"
                  },
                  "logs": [
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "RUNNINGnDuration: 60, Intensity: 1",
                      "log_update_datetime_utc": {
                        "$date": 1351282098750
                      },
                      "time": "2012-10-26 17:08:09 -0300",
                      "log_update_datetime": {
                        "$date": 1351292898000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "property_id": 297,
                          "value": "60"
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "property_id": 299,
                          "value": "1"
                        }
                      ],
                      "id": 380904
                    },
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "Running: Duration 60 minutes, Intensity 1 , Distance 1.0 kmnWith? Alone",
                      "log_update_datetime_utc": {
                        "$date": 1351282987710
                      },
                      "time": "2012-10-26 17:14:48 -0300",
                      "log_update_datetime": {
                        "$date": 1351293787000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "value": "60",
                          "property_id": 297
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "value": "1",
                          "property_id": 299
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 241561,
                          "value": "1.0",
                          "property_id": 241560
                        },
                        {
                          "loggable_id": 49,
                          "node_id": 432,
                          "value": "Alone",
                          "property_id": 431
                        }
                      ],
                      "id": 380906
                    },
                    {
                      "info": {
                        "type": "log"
                      },
                      "category": "exercise",
                      "text": "Running: Duration 60 minutes, Intensity 1 ; With? Alone",
                      "log_update_datetime_utc": {
                        "$date": 1351283100286
                      },
                      "time": "2012-10-26 17:24:48 -0300",
                      "log_update_datetime": {
                        "$date": 1351293900000
                      },
                      "nodes": [
                        {
                          "loggable_id": 296,
                          "node_id": 298,
                          "property_id": 297,
                          "value": "60"
                        },
                        {
                          "loggable_id": 296,
                          "node_id": 300,
                          "property_id": 299,
                          "value": "1"
                        },
                        {
                          "loggable_id": 49,
                          "node_id": 432,
                          "property_id": 431,
                          "value": "Alone"
                        }
                      ],
                      "id": 380907
                    }
                  ]
                }
              ]
            }

        """
        show_stats = self.get_argument("show_stats", False)
        categories = StrParser.parse_list(self.get_argument("roots", None))
        from_date = StrParser.parse_date(self.get_argument("from_date", None, True))
        direction = self.get_argument("direction", None)

        if show_stats:
            user_timeline = self._timeline_srv.get_user_timeline_with_daily_stats(user_id, categories, from_date, direction)

        else:
            user_timeline = self._timeline_srv.get_user_timeline(user_id, categories, from_date, direction)

        self.success(user_timeline, dev_message="Get Stream for User API")


@Deprecated(20130201)
@Route("/2/users/timeline/sync.json")
class SyncUserTimelineHandlerV2(BaseTimelineHandlerV2):
    """
    """

    def get(self):
        try:
            user_id = self.get_argument("user_id")
            client_last_sync_datetime_utc = DateParser.from_datetime(self.get_argument("last_sync_datetime_utc", None, True))

            dto = self._timeline_srv.sync_user_timeline(user_id, client_last_sync_datetime_utc)
            self.success("sync user timeline", dto)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/users/timeline/sync")
class SyncUserTimelineHandler(BaseTimelineHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        client_last_sync_datetime_utc = DateParser.from_datetime(self.get_argument("last_sync_datetime_utc", None, True))
        dto = self._timeline_srv.sync_user_timeline(user_id, client_last_sync_datetime_utc)
        self.success(dto, dev_message="sync user timeline")


routes = Route.get_routes()
