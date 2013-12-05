# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.oauth import authenticated


@Route("/test/account/create_autogenerated_account.json")
class CreateAutogeneratedAccountHandler(BaseHandler):

    def get(self):
        try:

            if self.get_argument("access_token") != "37cd33c21e2537d911ae65baddfd861231ec747151acc79d586f5b96c4364f1d":
                raise Exception("invalid access token")

            user_name_prefix = self.get_argument("user_name_prefix")
            account_srv = self._service_builder.build_account_service()
            created_user = account_srv.create_autogenerated_account(user_name_prefix)
            self.write(JSONParser.to_json(created_user))

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route("/test/auth/test/mytest/test/authenticate.test")
class TestAuthTestMyTestTestAuthenticateHandler(BaseHandler):

    @authenticated
    def get(self, user_id):
        print user_id

routes = Route.get_routes()
