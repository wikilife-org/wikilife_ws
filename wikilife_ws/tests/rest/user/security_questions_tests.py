"""
http://192.168.1.120:7090/1/account/security_questions/get/all.json
post: {"user_id":"2CXRMW","pin":"2222"}

request:  post: {"user_id":"2CXRMW","pin":"2222"}

response: {"status": "error", "message": "global name 'user_pin' is not defined", "data": null}
"""

# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest

class SecurityQuestionsTests(BaseTest):

    def test_create_sq(self):
        user = self.get_test_user()

        dto = {}
        dto["user_id"] = user["user_id"]
        dto["user_name"] = user["user_name"]
        dto["pin"] = user["pin"]
        dto["device_id"] = self.get_test_device_id()
        dto["security_questions"] = 

        url = self.get_service_url("/1/account/security_questions/edit.json") 
        body = JSONParser.to_json(dto)

        try:
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False
        
        expected_response = {"status": "OK", "message": "", "data": {"fields": {"status": 1, "server_id": 298, "map_id": "74376865", "parent": 297, "title": "Value Node", "namespace": "wikilife.exercise.exercise.running.duration.value-node", "update_time": {"$date": 1317417434980}, "slug": "value-node", "create_time": {"$date": 1307467723721}, "properties": {"log": False, "default": "60", "max_value": "600", "min_value": "0", "value_unit": "minutes", "value_type": "range", "multichild": False, "range_step": "5"}}, "model": "meta", "_id": 298, "pk": 298}}
        
        assert response != None
        assert response["status"] == expected_response["status"]
        assert response["message"] == expected_response["message"]
        assert response["data"]["pk"] == node_id


"""        
@Route('/1/account/security_questions/get/(?P<code>[-\w]+).json')
class UserGetSecurityQuestionRequestHandler(BaseSecurityQuestionHandler):

    @tornado.web.asynchronous
    def get(self, code):

    @tornado.web.asynchronous
    def post(self, code):
    
@Route('/1/account/security_questions/edit.json')
class UserEditSecurityQuestionRequestHandler(BaseSecurityQuestionHandler):

    @tornado.web.asynchronous
    def post(self):

@Route('/1/account/recovery/info.json')
class UserAccountRecoveryRequestHandler(BaseSecurityQuestionHandler):

    @tornado.web.asynchronous
    def post(self):
        
@Route('/1/account/reset/info.json')
class UserAccountResetRequestHandler(BaseSecurityQuestionHandler):

    @tornado.web.asynchronous
    def post(self, format):
"""        