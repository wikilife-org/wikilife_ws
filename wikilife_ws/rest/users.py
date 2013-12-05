# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless, authenticated
from wikilife_ws.utils.route import Route


class BaseUsersHandler(BaseHandler):

    _user_srv = None
    _oauth_srv = None
    _account_srv = None

    def initialize(self):
        super(BaseUsersHandler, self).initialize()
        self._user_srv = self._service_builder.build_user_service()
        self._oauth_srv = self._service_builder.build_oauth_service()
        self._account_srv = self._service_builder.build_account_service()

    def add_user_source(self, user, headers):
        if not "source" in user:
            user["source"] = self.get_source(headers)


@Route("/4/user/check/")
class UserNameCheckAvailabilityHandler(BaseUsersHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        user_name = self.get_argument(name="name", strip=True)
        dto = {}
        dto["userName"] = user_name
        dto["available"] = self._user_srv.is_username_available(user_name)
        self.success(dto)


@Route("/4/user/login/")
class UserLoginHandler(BaseUsersHandler):

    @userless
    @catch_exceptions
    def post(self):
        """
        Log in and retreive an authentication token.

        Request::

            {
              "userName": "qwerty"
              "pin": "1234",
            }

        Response::

            {
              oauth_token: ""
            }

        """
        user_credentials = JSONParser.to_collection(self.request.body)
        user_name = user_credentials["userName"]
        pin = user_credentials["pin"]
        oauth_token = self._oauth_srv.login(user_name, pin)

        if oauth_token != None:
            response = {"oauth_token": oauth_token}
            self.success(response, user_message="Login success")

        else:
            self.error(status_code=401, user_message="Login failed")


@Route("/4/user/name/")
class EditUserNameHandler(BaseUsersHandler):
    """
    """
    
    @authenticated
    @catch_exceptions
    def put(self, user_id):
        """
        Request::

            {
              "newUserName": "qwert2",
            }

        Response::
        """
        dto = JSONParser.to_collection(self.request.body)
        self._user_srv.edit_user_name(user_id, dto["newUserName"])
        self.success(user_message="User name changed successfully")


@Route("/4/user/pin/")
class EditPinHandler(BaseUsersHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def put(self, user_id):
        """
        Request::

            {
              "newPin": "2345",
            }

        Response::
        """
        dto = JSONParser.to_collection(self.request.body)
        self._user_srv.edit_pin(user_id, dto["newPin"])
        self.success(user_message="User pin changed successfully")


@Route("/4/user/account/")
class UserAccountHandler(BaseUsersHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Returns user account

        Response::

        {
            "userName": "TEST_qwerty323471",
            "status": 1,
            "profile": {
                "items": {
                    "city": {
                        "metricId": 209229,
                        "nodeId": 209228,
                        "value": "Buenos Aires"
                    },
                    "weight": {
                        "metricId": 209227,
                        "nodeId": 209226,
                        "value": 75
                    },
                    "gender": {
                        "metricId": 209238,
                        "nodeId": 209237,
                        "value": "Male"
                    },
                    "region": {
                        "metricId": 209233,
                        "nodeId": 209232,
                        "value": "Buenos Aires"
                    },
                    "birthdate": {
                        "metricId": 0,
                        "nodeId": 209234
                    },
                    "height": {
                        "metricId": 209223,
                        "nodeId": 209222,
                        "value": 1.8
                    },
                    "country": {
                        "metricId": 209231,
                        "nodeId": 209230,
                        "value": "Argentina"
                    }
                },
                "updateUTC": "2013-09-03 21:06:01"
            }
        }

        """
        dto = self._account_srv.get_account(user_id)
        self.success(dto)

    @userless
    @catch_exceptions
    def post(self):
        """
        Creates user account

        Request::

            {
              "userName": "docApi",
              "pin": "1234",
              "city": "Bahia Blanca",
              "timezone": "America\/Argentina\/San_Luis",
              "gender": "Male",
              "height": "1.70",
              "weight": "69.9",
              "device_id": "317a129728d554ff9e14dd72280fcf0000000000",
              "region": "Buenos Aires",
              "birthdate": "1995-10-29",
              "country": "ARG"
            }

        Response::

        """
        user_info = JSONParser.to_collection(self.request.body)
        self.add_user_source(user_info, self.request.headers)
        self._account_srv.create_account(user_info)
        self.success()


    @authenticated
    @catch_exceptions
    def delete(self, user_id):
        """
        Returns user account
        """
        self._account_srv.delete_account(user_id)
        self.success()


routes = Route.get_routes()
