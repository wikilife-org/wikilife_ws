# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.oauth import userless


class BaseLocationHandler(BaseHandler):

    _location_srv = None

    def initialize(self):
        super(BaseLocationHandler, self).initialize()
        self._location_srv = self._service_builder.build_location_service()


#@Route("/3/location/search")
class SearchHandler(BaseLocationHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        name = self.get_argument("name")
        country = self.get_argument("country", None)
        results = self._location_srv.search_location(name, country)
        self.success(results)


routes = Route.get_routes()