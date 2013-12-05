# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated
from wikilife_ws.utils.route import Route


class BaseDasniaHandler(BaseHandler):

    _devices_srv = None

    def initialize(self):
        super(BaseDasniaHandler, self).initialize()
        self._dasnia_srv = self._service_builder.build_dasnia_service()

@Route("/4/dasnia/services")
class AvailableDevicesHandler(BaseDasniaHandler):
    
    @authenticated
    @catch_exceptions
    def get(self):
        available_services = self._dasnia_srv.get_available_services()
        self.success(available_services)


@Route("/4/dasnia/users/services")
class UserServicesHandler(BaseDasniaHandler):

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        user_services = self._dasnia_srv.get_user_services(user_id)
        self.success(user_services)
    
    @authenticated
    @catch_exceptions
    def post(self, user_id):
        dto = JSONParser.to_collection(self.request.body)
        service_id = dto["service_id"]
        authorization_code = dto["auth_code"]
        added_user_service = self._dasnia_srv.add_service(user_id, service_id, authorization_code)
        self.success(added_user_service)


@Route("/4/dasnia/users/services/(?P<service_name>[-\w]+)")
class UsersDeleteServicesHandler(BaseDasniaHandler):

    @authenticated
    @catch_exceptions
    def delete(self, user_id, service_name):
        self._dasnia_srv.remove_service(user_id, service_name)
        self.success()


@Route("/4/dasnia/singly/push/(?P<hash>[-\w]+)")
class SinglyPushHandlerV2(BaseDasniaHandler):

    @catch_exceptions
    def post(self, hash):
        self._logger.info("## singly raw response: %s, hash %s" % (str(self.request.body), hash))
        dto = JSONParser.to_collection(self.request.body)
        self._dasnia_srv.process_singly_push(hash, dto)


routes = Route.get_routes()