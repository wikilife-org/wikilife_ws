# coding=utf-8

"""
Dummy services for infra config tests
"""

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.route import Route


@Route("/4/dummy")
class V4DummyHandler(BaseHandler):
    """
    """

    def get(self):
        self.success("V4 GET success")


@Route("/4/postdummy")
class V4PostDummyHandler(BaseHandler):
    """
    """

    def post(self):
        self.success("V4 POST Dummy success")


routes = Route.get_routes()
