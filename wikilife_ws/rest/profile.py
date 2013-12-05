# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.catch_exceptions import catch_exceptions


class BaseProfileHandler(BaseHandler):

    _profile_srv = None

    def initialize(self):
        super(BaseProfileHandler, self).initialize()
        self._profile_srv = self._service_builder.build_profile_service()


@Route("/3/users")
class UserProfileHandler(BaseProfileHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Returns a user's profile.

        Example::

            {
            "items": {
                "city": {
                    "node_id": 1166,
                    "value": null
                },
                "weight": {
                    "node_id": 1140,
                    "value": 22.6796185
                },
                "people": {
                    "node_id": 241600,
                    "value": null
                },
                "country": {
                    "node_id": 1162,
                    "value": "United States"
                },
                "region": {
                    "node_id": 1164,
                    "value": null
                },
                "eye-color": {
                    "node_id": 1145,
                    "value": null
                },
                "birthdate": {
                    "node_id": 1157,
                    "value": "1987-6-16"
                },
                "height": {
                    "node_id": 1142,
                    "value": 0.9144000000000001
                },
                "gender": {
                    "node_id": 1159,
                    "value": "Male"
                },
                "hair-color": {
                    "node_id": 1152,
                    "value": null
                },
                "skin-color": {
                    "node_id": 1147,
                    "value": null
                },
                "marital-status": {
                    "node_id": 1155,
                    "value": null
                },
                "ethnicity": {
                    "node_id": 1170,
                    "value": null
                }
            },
            "user_id": "IJFDUC"
        }

        * *items* is an object containing several pairs of node_ids and values.
        Each node_id refers to the value node within wikilife's graph that
        models that particular value.  TODO: SEE META!
        """
        profile = self._profile_srv.get_profile(user_id)
        self.success(profile)


routes = Route.get_routes()
