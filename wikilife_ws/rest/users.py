# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import userless, authenticated


class UserNameCheckAvailabilityHandler(BaseHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        user_srv = self._services["user"]
        user_name = self.get_argument(name="name", strip=True)
        dto = {}
        dto["userName"] = user_name
        dto["available"] = user_srv.is_username_available(user_name)
        self.success(dto)


class UserLoginHandler(BaseHandler):

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
        oauth_srv = self._services["oauth"]
        user_credentials = JSONParser.to_collection(self.request.body)
        user_name = user_credentials["userName"]
        pin = user_credentials["pin"]
        oauth_token = oauth_srv.login(user_name, pin)

        if oauth_token != None:
            response = {"oauth_token": oauth_token}
            self.success(response, user_message="Login success")

        else:
            self.error(status_code=401, user_message="Login failed")


class EditUserNameHandler(BaseHandler):
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
        user_srv = self._services["user"]
        dto = JSONParser.to_collection(self.request.body)
        user_srv.edit_user_name(user_id, dto["newUserName"])
        self.success(user_message="User name changed successfully")


class EditPinHandler(BaseHandler):
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
        user_srv = self._services["user"]
        dto = JSONParser.to_collection(self.request.body)
        user_srv.edit_pin(user_id, dto["newPin"])
        self.success(user_message="User pin changed successfully")


class UserAccountHandler(BaseHandler):
    """
    """

    def add_user_source(self, user, headers):
        if not "source" in user:
            user["source"] = self.get_source(headers)

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
        account_srv = self._services["account"]
        dto = account_srv.get_account(user_id)
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
        account_srv = self._services["account"]
        user_info = JSONParser.to_collection(self.request.body)
        self.add_user_source(user_info, self.request.headers)
        account_srv.create_account(user_info)
        self.success()


    @authenticated
    @catch_exceptions
    def delete(self, user_id):
        """
        Deletes user account
        """
        account_srv = self._services["account"]
        account_srv.delete_account(user_id)
        self.success()


class UserProfileHandler(BaseHandler):
    """
    """

    #@authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Returns user's profile.

        Example::
        {
        "userId": "",
        "items" : {
            "gender": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "birthdate": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "height": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "weight": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "country": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "region": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")},
            "city": {"nodeId": 0, "metricId": 0, value: "", "updateUTC": ISODate("")}
            }
        }

        * *items* is an object containing several pairs of node ids and values.
        Each node id refers to the value node within wikilife's graph that
        models that particular value.  TODO: SEE META!
        """
        profile_srv = self._services["profile"]
        profile = profile_srv.get_profile(user_id)
        self.success(profile)
