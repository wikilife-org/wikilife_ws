# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated_developer
from wikilife_ws.utils.route import Route


class BaseOauthHandler(BaseHandler):

    _app_srv = None

    def initialize(self):
        BaseHandler.initialize(self)
        self._app_srv = self._service_builder.build_app_service()
        self._user_srv = self._service_builder.build_user_service()
        self._oauth_srv = self._service_builder.build_oauth_service()

    def get_developer_for_token(self, token):
        return self._service_builder.build_developer_service().get_developer_for_token(token)


@Route("/3/oauth/developers/apps")
class AppsHandler(BaseOauthHandler):

    @authenticated_developer
    @catch_exceptions
    def get(self, developer_id):
        """
        Get developer apps
        """
        apps = self._app_srv.get_apps_by_developer(developer_id)
        self.success(apps)

    @authenticated_developer
    @catch_exceptions
    def post(self, developer_id):
        """
        Add app
        """
        dto = JSONParser.to_collection(self.sanitize_raw_data(self.request.body))
        app = self._app_srv.add_app(dto["name"], dto["callbackUrl"], developer_id)
        self.success(app)


@Route("/3/oauth/developers/apps/(?P<app_id>[-\w]+)")
class AppHandler(BaseOauthHandler):

    @authenticated_developer
    @catch_exceptions
    def put(self, app_id, developer_id):
        """
        Update app
        """
        dto = JSONParser.to_collection(self.sanitize_raw_data(self.request.body))
        updated_app = self._app_srv.update_app(app_id, dto["name"], dto["callbackUrl"], developer_id)
        self.success(updated_app)

    @authenticated_developer
    @catch_exceptions
    def delete(self, app_id, developer_id):
        """
        Remove app
        """
        #developer_id just a tmp double check
        self._app_srv.remove_app(app_id, developer_id)
        self.success()


@Route("/oauth2/authorize")
class AuthorizeHandler(BaseOauthHandler):

    def get(self):
        """
        Get oauth form
        """

        params = self.get_params()
        try:
            client_id = params["client_id"]
        except Exception:
            self.write("client_id is mandatory")
        #validar client_id
        app = self._app_srv.get_app_by_client_id(client_id)
        error = ""
        if app == None:
            error = "Invalid client_id"

        response_type = params["response_type"]
        redirect_uri = params["redirect_uri"]

        self.render("oauth/login.html", response_type=response_type, redirect_uri=redirect_uri, client_id=client_id, error=error,)

    def post(self):
        """
        Authorize App
        """

        params = self.get_params()
        user_name = params["user_name"]
        pin = params["pin"]
        response_type = params["response_type"]
        redirect_uri = params["redirect_uri"]
        client_id = params["client_id"]
        #validate
        try:
            user = self._user_srv.find_user({"user_name": user_name, "pin": pin})
        except Exception:
            self.render("oauth_form.html", response_type=response_type, redirect_uri=redirect_uri, error=True, client_id=client_id)

        token, code = self._oauth_srv.authorize(user["user_id"], client_id)

        parameter = "access_token=%s&user_id=%s" % (token, user["user_id"])
        if response_type == "code":
            parameter = "code=%s" % code

        self.redirect(redirect_uri + "?" + parameter)


@Route("/oauth2/access_token")
class AccessTokenHandler(BaseOauthHandler):

    def get(self):
        """
        Get token
        """

        params = self.get_params()
        try:
            client_id = params["client_id"]
        except Exception:
            self.write("client_id is mandatory")

        #validar client_id
        app = self._app_srv.get_app_by_client_id(client_id)
        if app == None:
            self.write("Invalid client_id")

        #grant_type = params["grant_type"]
        code = params["code"]
        token = self._oauth_srv.get_token_for_code(code, client_id)
        user_id = self._oauth_srv.get_user_for_token(token)
        response = {"access_token": token, "user_id": user_id}
        self.success(response, user_message="Access Token Request")


routes = Route.get_routes()
