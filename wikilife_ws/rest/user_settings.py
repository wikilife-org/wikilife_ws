# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.deprecated import Deprecated


class BaseUserSettingsHandler(BaseHandler):

    _twitter_user_srv = None

    def initialize(self):
        super(BaseUserSettingsHandler, self).initialize()
        self._twitter_user_srv = self._service_builder.build_twitter_user_service()


@Route('/3/settings/twitter')
class SettingsTwitterRequestHandler(BaseUserSettingsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Response:
        {
            "apis": {
                "twitter": {
                    "active": "true",
                    "roots": [
                        "mood",
                        "CAT-SLUG"
                    ]
                }
            }
        }
        """

        twitter_settings = self._twitter_user_srv.get_twitter_settings(user_id)
        self.success(twitter_settings)

    @authenticated
    @catch_exceptions
    def post(self, user_id):
        """
        Request body:
        {"roots":[""],"active":True,"access_token_secret":"","access_token_key":""}
        """

        twitter_settings = JSONParser.to_collection(self.request.body)
        self._twitter_user_srv.set_twitter_settings(user_id, twitter_settings)
        self.success()


routes = Route.get_routes()
