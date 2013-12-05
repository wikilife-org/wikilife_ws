# coding=utf-8

from wikilife_ws.tests.base_ws_test import BaseWSTest, TEST_USER_ID
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import STATUS_SUCCESS


class NotificationTests(BaseWSTest):
    """
    Requirements:

    1. A running TEST environment:
    /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    /wikilife_ws/server-start.sh 7080 local

    """

    def test_get_update_notification(self):

        url = self.get_service_url("/1/notifications.json")
        params = {}

        #invoke ws
        try:
            raw_response = self.rest_get(url, params)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "Notification Service"
        assert response["data"] == [{"mandatory": True, "message": "Recommended application update", "code": "sys_update", "type": "system", "params": {"url": "http://itunes.apple.com/ca/app/wikilife/id443072007?mt=8"}}]

    def test_get_notification(self):

        url = self.get_service_url("/1/notifications.json")
        params = {"client_id": "317A1297-28D5-54FF-9E14-DD72280FCF00", "client_version": "0.9.1.6", "client_tree_version": "meta_11.0.0", "client_api_version": "R11.0.0"}

        #invoke ws
        try:
            raw_response = self.rest_get(url, params)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "Notification Service"
        assert response["data"] == []
