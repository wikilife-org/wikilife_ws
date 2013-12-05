# coding=utf-8

from wikilife_biz.services.user.security_question_service import \
    SecurityQuestionsServiceException
from wikilife_biz.services.user.user_service import UserServiceException
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler, BaseHandlerV2
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.oauth import authenticated, userless
from wikilife_ws.utils.route import Route
from wikilife_ws.utils.deprecated import Deprecated


class BaseSecurityQuestionHandler(BaseHandler):

    _user_srv = None
    _sq_srv = None

    def initialize(self):
        super(BaseSecurityQuestionHandler, self).initialize()
        self._user_srv = self._service_builder.build_user_service()
        self._sq_srv = self._service_builder.build_security_question_service()

class BaseSecurityQuestionHandlerV2(BaseHandlerV2):

    _user_srv = None
    _sq_srv = None

    def initialize(self):
        super(BaseSecurityQuestionHandlerV2, self).initialize()
        self._user_srv = self._service_builder.build_user_service()
        self._sq_srv = self._service_builder.build_security_question_service()


@Deprecated(20130201)
@Route('/1/account/security_questions/get/(?P<code>[-\w]+).json')
class UserGetSecurityQuestionRequestHandlerV2(BaseSecurityQuestionHandlerV2):
    """
    """

    def get(self, code):
        try:
            sq = self._sq_srv.get_security_questions(code)
            self.success("Get Security Questions API", sq)

        except Exception, e:

            self._logger.error(e)
            self.error(str(e))

    def post(self, code):
        try:
            ar_info = JSONParser.to_collection(self.request.body)
            user_id = ar_info["user_id"]
            pin = ar_info["pin"]

            self._user_srv.validate_user_pin(user_id, pin)
            sq = self._sq_srv.get_security_questions_with_answers(code, user_id)
            self.success("Get Security Questions API", sq)

        except UserServiceException, e:
            self.error(str(e))

        except SecurityQuestionsServiceException, e:
            self.success(str(e), [])

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route('/3/account/security_questions/(?P<code>[-\w]+)')
class SecurityQuestionsRequestHandler(BaseSecurityQuestionHandler):
    """
    """

    @catch_exceptions
    def get(self, code):
        sq = self._sq_srv.get_security_questions(code)
        self.success(sq)


@Route('/3/account/user/security_questions/(?P<code>[-\w]+)')
class UserSecurityQuestionsRequestHandler(BaseSecurityQuestionHandler):
    """
    """
    
    @authenticated
    @catch_exceptions
    def get(self, user_id, code):
        try:
            user_sq = self._sq_srv.get_security_questions_with_answers(code, user_id)
            self.success(user_sq)

        except UserServiceException, e:
            self.error(str(e))

        except SecurityQuestionsServiceException, e:
            self.success(str(e), [])


@Deprecated(20130201)
@Route('/1/account/security_questions/edit.json')
class UserEditSecurityQuestionRequestHandlerV2(BaseSecurityQuestionHandlerV2):
    """
    """

    def post(self):
        try:
            sc_update = JSONParser.to_collection(self.request.body)

            user_id = sc_update["user_id"]
            user_name = sc_update["user_name"]
            pin = sc_update["pin"]
            security_questions = sc_update["security_questions"]
            device_id = sc_update["device_id"]

            self._user_srv.validate_user(user_id, user_name, pin)
            self._sq_srv.validate_security_questions(security_questions)
            self._sq_srv.update_user_recovery_information(user_id, device_id, security_questions)

            self.success("Edit Security Questions API")

        except UserServiceException, e:
            self.error(str(e))

        except SecurityQuestionsServiceException, e:
            self.error(str(e))

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route('/3/account/user/security_questions')
class UserEditSecurityQuestionRequestHandler(BaseSecurityQuestionHandler):
    """
    """
    
    @authenticated
    @catch_exceptions
    def put(self, user_id):
        sc_update = JSONParser.to_collection(self.request.body)
        security_questions = sc_update["security_questions"]
        device_id = sc_update["device_id"]
        self._sq_srv.validate_security_questions(security_questions)
        self._sq_srv.update_user_recovery_information(user_id, device_id, security_questions)
        self.success()


@Deprecated(20130201)
@Route('/1/account/recovery/info.json')
class UserAccountRecoveryRequestHandlerV2(BaseSecurityQuestionHandlerV2):
    """
    """

    def post(self):
        try:
            ar_info = JSONParser.to_collection(self.request.body)

            device_id = ar_info.get("device_id", None)
            security_questions = ar_info["security_questions"]
            birthdate = ar_info["birthdate"]

            data = self._sq_srv.find_user_recovery_info_with_device_id(birthdate, device_id, security_questions)

            self.success("Account Recovery Service", [data])

        except SecurityQuestionsServiceException, e:
            self.success(str(e), [])

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route('/3/account/user/recovery')
class UserAccountRecoveryRequestHandler(BaseSecurityQuestionHandler):
    """
    """

    @userless
    @catch_exceptions
    def post(self):
        try:
            ar_info = JSONParser.to_collection(self.request.body)
            device_id = ar_info.get("device_id", None)
            security_questions = ar_info["security_questions"]
            birthdate = ar_info["birthdate"]
            data = self._sq_srv.find_user_recovery_info_with_device_id(birthdate, device_id, security_questions)
            self.success([data])

        except SecurityQuestionsServiceException, e:
            self.success([], dev_message=str(e))


@Deprecated(20130201)
@Route('/1/account/reset/info.json')
class UserAccountResetRequestHandlerV2(BaseSecurityQuestionHandlerV2):
    """
    """

    def post(self):
        try:
            ar_info = JSONParser.to_collection(self.request.body)

            user_id = ar_info["user_id"]
            token = ar_info["token"]
            new_username = ar_info["new_username"]
            new_pin = ar_info["new_pin"]

            self._sq_srv.reset_user_credentials(user_id, token, new_username, new_pin)
            self.success("Reset Credentials Service")

        except SecurityQuestionsServiceException, e:
            self.error(str(e))

        except Exception, e:
            self._logger.error(e)
            self.error(str(e))


@Route('/3/account/user/reset')
class UserAccountResetRequestHandler(BaseSecurityQuestionHandler):
    """
    """
    
    @authenticated
    @catch_exceptions
    def post(self ,user_id):
        try:
            ar_info = JSONParser.to_collection(self.request.body)
            token = ar_info["token"]
            new_username = ar_info["new_username"]
            new_pin = ar_info["new_pin"]

            self._sq_srv.reset_user_credentials(user_id, token, new_username, new_pin)
            self.success()

        except SecurityQuestionsServiceException, e:
            self.error(str(e))


routes = Route.get_routes()
