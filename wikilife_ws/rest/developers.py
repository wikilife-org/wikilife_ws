# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.route import Route


class BaseDeveloperHandler(BaseHandler):

    _developer_srv = None

    def initialize(self):
        super(BaseDeveloperHandler, self).initialize()
        self._developer_srv = self._service_builder.build_developer_service()


@Route('/4/oauth/developers/sessions')
class SessionHandler(BaseDeveloperHandler):
    """
    """

    @catch_exceptions
    def post(self):
        """
        Response::
                {
                   developerName: <username>,
                   developerId: <user_id>,
                   session: <session_id>
                }

        """
        params = JSONParser.to_collection(self.request.body)
        developer = self._developer_srv.validate_developer_credentials(params["developerName"], params["password"])
        token = self._developer_srv.get_session_token(developer["developerId"])
        response = {"developerId": developer["developerId"], "developerId": developer["developerId"], "session": token}
        self.success(response, user_message="Login successful")

    @catch_exceptions
    def delete(self):
        params = self.get_params()
        self._developer_srv.remove_session(params["developerId"], params["session_token"])
        self.success(user_message="Delete session successful")


@Route('/4/oauth/developers/')
class DeveloperRequestHandler(BaseDeveloperHandler):
    """
    """

    @catch_exceptions
    def post(self):
        """
        Response::
            {
               developerName: <username>,
               developerId: <user_id>,          
               session: <session_id>
            }

        """
        params = JSONParser.to_collection(self.request.body)
        developer = self._developer_srv.create_developer(params["developerName"], params["password"], params["email"])
        token = self._developer_srv.get_session_token(developer["developerId"])
        response = {"developerId": developer["developerId"], "developerName":developer["developerName"], "session":token}
        self.success(response, user_message="Registration successful") 


routes = Route.get_routes()