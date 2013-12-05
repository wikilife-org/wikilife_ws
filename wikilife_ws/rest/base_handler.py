# coding=utf-8

import tornado
from tornado.web import RequestHandler
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.utils.app_ctx import AppCTX


class BaseHandler(RequestHandler):

    _logger = None
    _service_builder = None

    def initialize(self):
        #RequestHandler.initialize(self)
        super(BaseHandler, self).initialize()
        #TODO get this dependecies injected
        app_ctx = AppCTX.get_instance()
        self._logger = app_ctx.logger
        self._service_builder = app_ctx.service_builder

    def get_user_for_token(self, token):
        return self._service_builder.build_oauth_service().get_user_for_token(token)

    def set_default_headers(self):
        self.set_header("Server", "WikilifeAPI tornado/{}".format(tornado.version))
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Max-Age", 86400)

    def get_source(self, headers):
        #WikiLife/1.0.0.7 CFNetwork/485.2 Darwin/10.8.0
        source = "client.unknown"

        if "User-Agent" in headers:
            user_agent = str(headers["User-Agent"]).lower()

            if "wikilife" in user_agent:
                source = "client.iphone"
            else:
                source = "client.other: %s" % user_agent

        return source

    def sanitize_raw_data(self, raw_data):
        tmp = str(raw_data).replace('\\"', '')
        return str(tmp).replace("\\", "")

    def _json(self, status_code, message, data):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        response = JSONParser.to_json({"status": status_code, "message": message, "data": data})
        self.write(response)

    def get_params(self):
        arguments = self.request.arguments
        params = {}
        for key in arguments:
            params[key] = arguments[key][0]

        return params

    def get_str_params(self):
        arguments = self.request.arguments
        params = {}
        for key in arguments:
            params[key] = str(arguments[key][0])

        return params

    def success(self, response=None, status_code=200, user_message=None, dev_message=None):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        if user_message is not None:
            self.set_header("X-User-Message", user_message)
        if dev_message is not None:
            self.set_header("X-Dev-Message", dev_message)
        self.write(JSONParser.to_json(response))

    def error(self, error="", user_message=None, dev_message=None, status_code=500):
        self._logger.error(error)

        if user_message is not None:
            self.set_header("X-User-Message", user_message)
        if dev_message is not None:
            self.set_header("X-Dev-Message", dev_message)
        self.set_status(status_code)
        self.finish()
