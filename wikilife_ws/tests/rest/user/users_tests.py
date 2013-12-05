# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest, TEST_USER_NAME, \
    TEST_USER_PIN, TEST_USER_ID
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import STATUS_SUCCESS


class UsersTests(BaseTest):
    """
    Requirements:

    1. A running TEST environment:
    /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    /wikilife_processors/server-start.sh local
    /wikilife_ws/server-start.sh 7080 local

    2. Test users:
    test1 full active user
    test1000 to test9999 available user names
    """

    def test_validate_user_name(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/account/username/validate.json
        POST:
        {"user_name": "test777"}

        RESP:
        {"status": "OK", "message": "User name is available"}
        """

        url = self.get_service_url("/1/account/username/validate.json")
        user_info = {"user_name": "test1000"}

        #invoke ws
        try:
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "User name is available"
        assert response["data"] == None

    def test_find_user(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/account/validate.json
        POST:
        {"device_id":"317A1297-28D5-54FF-9E14DD72280FCF00","pin":"7777","user_name":"test776"}

        RESP:
        {"status": "ERROR", "message": "Invalid PIN Number"}
        """

        url = self.get_service_url("/1/account/validate.json")
        user_info = {"user_name": TEST_USER_NAME, "pin": TEST_USER_PIN}

        #invoke ws
        try:
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == ""
        assert response["data"] != None
        user_info = response["data"]
        assert user_info["user_id"] == TEST_USER_ID
        assert user_info["user_name"] == TEST_USER_NAME
        assert user_info["pin"] == TEST_USER_PIN

    def test_get_user_profile(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/users/show/CSQTMG.json
        GET

        RESP:
        {"fields": {"items": [{"title": "Weight", "value": "69.9", "properties": {"log": true, "default": "70.0", "max_value": "250.0", "min_value": "1.0", "value_type": "range", "range_step": "0.1", "value_unit": "kg"}, "node_id": 1140, "slug": "weight"}, {"slug": "height", "title": "Height", "value": "1.70", "node_id": 1142, "properties": {"log": true, "default": "1.70", "max_value": "2.50", "min_value": "0.01", "value_type": "range",  "range_step": "0.01", "value_unit": "m"}}, {"title": "Eye Color", "value": "", "slug": "eye-color", "node_id": 1145, "properties": {"default": "Brown", "log": true, "value_type": "text", "options": ["Black", "Amber", "Blue", "Brown", "Gray", "Green", "Hazel", "Red"]}}, {"title": "Skin Color", "value": "", "slug": "skin-color", "node_id": 1147, "properties": {"default": "Light Intermediate", "log": true, "value_type": "text",  "options": ["Very Light", "Light", "Light Intermediate", "Dark Intermediate", "Dark", "Very Dark"]}}, {"title": "Hair Amount", "value": "", "slug": "hair-amount", "node_id": 1150, "properties": {"default": "Intermediate", "log": true, "value_type": "text", "options": ["Abundant", "Intermediate", "Too Little", "Bald"]}}, {"title": "Hair Color", "value": "", "slug": "hair-color", "node_id": 1152, "properties": {"default": "Brown", "log": true, "value_type": "text",  "options": ["Black", "Brown", "Auburn", "Chestnut", "Red", "Blond", "Gray", "White"]}}, {"slug": "marital-status", "title": "Life Partners", "value": "", "properties": {"default": "Single", "options": ["Single", "Married", "Boyfriend", "Girlfriend", "Lover"], "value_type": "text", "log": true}, "node_id": 1155}, {"title": "Birthdate", "slug": "birthdate", "node_id": 1157, "value": "1986-02-15", "properties": {"value_type": "datetime", "log": true}, {"title": "Gender", "value": "Male", "slug": "gender", "node_id": 1159, "properties": {"default": "Male", "log": true, "value_type": "text",  "options": ["Male", "Female"]}}, {"title": "Country", "value": "ARG", "slug": "country", "node_id": 1162, "properties": {"value_type": "text", "log": true}}, {"title": "Region", "value": "Buenos Aires", "slug": "region", "node_id": 1164, "properties": {"value_type": "text", "log": true}}, {"title": "City", "value": "Bahia Blanca", "slug": "city", "node_id": 1166, "properties": {"value_type": "text", "log": true}}, {"title": "Ethnicity", "value": "", "slug": "ethnicity", "node_id": 1170, "properties": {"default": "Caucasian-hispanic", "options": ["Caucasian-hispanic", "Caucasian-nonhispanic", "African American", "Asian", "American Indian/Alaskan Native", "Native Hawaiian"], "value_type": "text", "log": true}}, {"title": "Living With", "value": "", "slug": "living-with", "node_id": 241459, "properties": {"default_property": true, "property": true, "log": false}}], "user_id": "CSQTMG", "avatar": "/static/images/avatars/male_8.png", "user_name": "test777"}, "create_time": "15-02-2012 14:48:09", "model": "Profile"}
        """

        url = self.get_service_url("/1/users/show/%s.json" % TEST_USER_NAME)

        #invoke ws
        try:
            raw_response = self.rest_get(url)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == ""
        assert response["data"] != None
        profile = response["data"]
        assert "model" in profile and profile["model"] == "Profile"
        assert "fields" in profile
        assert profile["fields"]["user_id"] == TEST_USER_NAME

    def test_add_account(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/account/add.json
        POST:
        {
           "city":"Bahia Blanca",
           "timezone":"America/Argentina/San_Luis",
           "weight":"69.9",
           "device_id":"317A1297-28D5-54FF-9E14-DD72280FCF00",
           "region":"Buenos Aires",
           "birthdate":"1986-02-15",
           "user_id":"",
           "height":"1.70",
           "gender":"Male",
           "security_questions":[
              {
                 "pk":"SQ_FRND",
                 "answer":"q1"
              },
              {
                 "pk":"SQ_STR",
                 "answer":"q2"
              },
              {
                 "pk":"SQ_JOB",
                 "answer":"q3"
              },
              {
                 "pk":"SQ_MMN",
                 "answer":"q4"
              },
              {
                 "pk":"SQ_FYB",
                 "answer":"q5"
              }
           ],
           "country":"ARG",
           "user_name":"test777",
           "pin":"7777"
        }

        RESP:
        {
           "private_user_id":"KCVLAP",
           "user_id":"CSQTMG",
           "user_name":"test777",
           "pin":"7777"
        }
        """

        url = self.get_service_url("/1/account/add.json")
        user_name = "test2000"
        pin = "1234"
        account_user_info = {
            "city": "Bahia Blanca",
            "timezone": "America/Argentina/San_Luis",
            "weight": "100.0",
            "device_id": "317A1297-28D5-54FF-9E14-DD72280FCF00",
            "region": "Buenos Aires",
            "birthdate": "1980-12-12",
            "user_id": "",
            "height": "2.0",
            "gender": "Male",
            "security_questions": [
                {
                    "pk": "SQ_FRND",
                    "answer": "q1"
                }, {
                    "pk":"SQ_STR",
                    "answer":"q2"
                }, {
                    "pk":"SQ_JOB",
                    "answer":"q3"
                }, {
                    "pk":"SQ_MMN",
                    "answer":"q4"
                }, {
                    "pk":"SQ_FYB",
                    "answer":"q5"
                }
            ],
            "country": "ARG",
            "user_name": user_name,
            "pin": pin
        }

        #invoke ws
        try:
            body = JSONParser.to_json(account_user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == "success"
        assert response["message"] == ""
        assert response["data"] != None
        user_info = response["data"]
        assert "user_name" in user_info and user_info["user_name"] == user_name
        assert "pin" in user_info and user_info["pin"] == pin
        assert "user_id" in user_info and len(user_info["user_id"]) > 0

    def test_edit_user_name(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/account/username/edit.json...
        POST:
        {"pin": "7777", "user_id": "CSQTMG", "new_user_name": "test776"}

        RESP:
        {"status": "OK", "message": "User name changed successfully"}
        """

        url = self.get_service_url("/1/account/username/edit.json")
        new_user_name = "%s_upd" % TEST_USER_NAME
        user_info = {"user_id": TEST_USER_NAME, "pin": TEST_USER_NAME, "new_user_name": new_user_name}

        #invoke ws
        try:
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "User name changed successfully"
        assert response["data"] == None

        #restore user_name
        try:
            user_info = {"user_id": TEST_USER_NAME, "pin": TEST_USER_NAME, "new_user_name": TEST_USER_NAME}
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "User name changed successfully"
        assert response["data"] == None

    def test_edit_pin(self):
        """
        Sample API-1 request/response:

        http://qaapi.wikilife.org/1/account/pin/edit.json
        POST:
        {"pin": "7777", "user_id": "CSQTMG", "new_pin": "7776"}

        RESP:
        {"status": "OK", "message": "User pin changed successfully"}
        """

        url = self.get_service_url("/1/account/pin/edit.json")
        new_pin = "%s_upd" % TEST_USER_NAME
        user_info = {"user_id": TEST_USER_NAME, "pin": TEST_USER_NAME, "new_pin": new_pin}

        #invoke ws
        try:
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "User pin changed successfully"
        assert response["data"] == None

        #restore pin
        try:
            user_info = {"user_id": TEST_USER_NAME, "pin": new_pin, "new_pin": TEST_USER_NAME}
            body = JSONParser.to_json(user_info)
            raw_response = self.rest_post(url, body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "User pin changed successfully"
        assert response["data"] == None
