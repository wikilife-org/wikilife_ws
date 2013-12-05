# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler, BaseHandlerV2
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.deprecated import Deprecated
from wikilife_ws.utils.route import Route

USER_STATS_BY_TAG = 5
USER_STATS_BY_QUESTION = 6


class BaseNotificationHandlerV2(BaseHandlerV2):

    _notification_srv = None

    def initialize(self):
        super(BaseNotificationHandlerV2, self).initialize()
        self._notification_srv = self._service_builder.build_notification_service()


class BaseNotificationHandler(BaseHandler):

    _notification_srv = None

    def initialize(self):
        super(BaseNotificationHandler, self).initialize()
        self._notification_srv = self._service_builder.build_notification_service()


@Deprecated(20130201)
@Route('/1/notifications')
@Route('/1/notifications.json')
class NotificationstHandlerV2(BaseNotificationHandlerV2):
    """
    """

    def get(self):
        """
        Request:

        GET /notifications

        {
            lang: String. ISO 639-1 code. e.g: "es", "en", "pt".
            user_id: String. e.g: "CKJG3L".
            client_id: String. This id/code is unique for each registered client. e.g: "iphone_core_client".
            client_version: String. major.minor.stage.build  http://en.wikipedia.org/wiki/Software_versioning#Designating_development_stage  e.g: 1.4.3.25.
            client_tree_version: String. Tree version used by the client.
            client_api_version: String. REST API version used by the client.
        }

        Response::

        The response is a JSON notifications list  [{}]

        Notification fields:

        type: String. Required. Current valid options: "system", "user".
        code: String. Required. Current valid options: "sys_update", "usr_msg", "usr_confirm".
        mandatory: Boolean. Required. If true, client blocks until user take action. If false user can skip it.
        message: String. Required. Localized notificacion human readable message. Language is determined by lang request param.
        params: Object (dictionary). Optional. Notificacion parameters. Parameters are different for each notification type/code.

        TODO analyse:
        notificaction id/pk to check consumed notifications


        Samples:

        [
         {type: "system", code: "sys_update", mandatory: true, message: "Required application update", params: {url: "http://"}},
         {type: "user", code: "usr_msg", mandatory: false, message: "Hey buddy!, long time without logging food, are you still alive ?"}
        ]

        [
         {type: "system", code: "sys_update", mandatory: false, message: "Recommended application update", params: {url: "http://"}},
         {type: "user", code: "usr_msg", mandatory: false, message: "Your excercise budget for today is ****"
        ]

        Dummy service impl.
        """

        try:
            user_id = self.get_argument("user_id", None)
            lang = self.get_argument("lang", 'en')
            client_id = self.get_argument("client_id")
            client_version = self.get_argument("client_version")
            client_tree_version = self.get_argument("client_tree_version")
            client_api_version = self.get_argument("client_api_version")
            self._notification_srv.get_notifications(client_id, client_version, client_tree_version, client_api_version, lang, user_id)

        except Exception:
            self._notification_srv.get_update_notification()

        finally:
            self.write("[]")


@Route('/3/notifications')
class NotificationstHandler(BaseNotificationHandler):
    """
    """
    
    @catch_exceptions
    def get(self):
        """
        Request:

        GET /notifications

        {
            lang: String. ISO 639-1 code. e.g: "es", "en", "pt".
            user_id: String. e.g: "CKJG3L".
            client_id: String. This id/code is unique for each registered client. e.g: "iphone_core_client".
            client_version: String. major.minor.stage.build  http://en.wikipedia.org/wiki/Software_versioning#Designating_development_stage  e.g: 1.4.3.25.
            client_tree_version: String. Tree version used by the client.
            client_api_version: String. REST API version used by the client.
        }

        Response::

        The response is a JSON notifications list  [{}]

        Notification fields:

        type: String. Required. Current valid options: "system", "user".
        code: String. Required. Current valid options: "sys_update", "usr_msg", "usr_confirm".
        mandatory: Boolean. Required. If true, client blocks until user take action. If false user can skip it.
        message: String. Required. Localized notificacion human readable message. Language is determined by lang request param.
        params: Object (dictionary). Optional. Notificacion parameters. Parameters are different for each notification type/code.

        TODO analyse:
        notificaction id/pk to check consumed notifications


        Samples:

        [
         {type: "system", code: "sys_update", mandatory: true, message: "Required application update", params: {url: "http://"}},
         {type: "user", code: "usr_msg", mandatory: false, message: "Hey buddy!, long time without logging food, are you still alive ?"}
        ]

        [
         {type: "system", code: "sys_update", mandatory: false, message: "Recommended application update", params: {url: "http://"}},
         {type: "user", code: "usr_msg", mandatory: false, message: "Your excercise budget for today is ****"
        ]

        Dummy service impl.
        """

        user_id = self.get_argument("user_id", None)
        lang = self.get_argument("lang", 'en')
        client_id = self.get_argument("client_id")
        client_version = self.get_argument("client_version")
        client_tree_version = self.get_argument("client_tree_version")
        client_api_version = self.get_argument("client_api_version")
        self._notification_srv.get_notifications(client_id, client_version, client_tree_version, client_api_version, lang, user_id)
        
        #mock
        response = []
        
        self.success(response)


routes = Route.get_routes()
