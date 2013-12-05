# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest


class AccountTests(BaseTest):
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
        user_name = "test2123"
        pin = "1234"
        account_user_info = {"city": "Bahia Blanca", "timezone": "America/Argentina/San_Luis", "weight": "100.0", "device_id": "317A1297-28D5-54FF-9E14-DD72280FCF00", "region": "Buenos Aires", "birthdate": "1980-12-12", "user_id": "", "height": "2.0", "gender": "Male", "security_questions": [{"pk": "SQ_FRND", "answer": " q1"}, {"pk": "SQ_STR", "answer": "q2"}, {"pk": "SQ_JOB", "answer": "q3"}, {"pk": "SQ_MMN", "answer": "q4"}, {"pk": "SQ_FYB", "answer": "q5"}], "country": "ARG", "user_name": user_name, "pin": pin}

        #invoke ws
        try:
            body = JSONParser.to_json(account_user_info)
            raw_response = self.rest_post(url, body)
            print "raw_response: %s" % raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == 1
        assert response["user_name"] == user_name
