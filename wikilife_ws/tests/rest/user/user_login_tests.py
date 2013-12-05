# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest
from wikilife_utils.parsers.json_parser import JSONParser

TEST_USER = {"username" : "asdfghij", "pin" : "1234", "userId" : "X6Q4WT", "token" : "RQe3vywoYSBi6GaiAnCvLhd5", "clientId" : "dbscript.iphone"}


class UserLoginTests(BaseTest):

    def test_login(self):

        user_credentials = {
            "username": TEST_USER["username"],
            "pin": TEST_USER["pin"]
        }

        #invoke ws
        try:
            url = "http://localhost:7080/3/account/login"
            body = JSONParser.to_json(user_credentials)
            
            response_code, response_headers, response_body = self.rest_post(url, body)
            print response_code
            print response_headers
            print response_body
            response_body_json = JSONParser.to_collection(response_body)

        except Exception, e:
            print e
            assert False

        assert response_code == 200
        assert response_body_json["oauth_token"] == TEST_USER["token"]
