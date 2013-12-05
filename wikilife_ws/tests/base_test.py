# coding=utf-8

from wikilife_data.utils.db_conn import DBConn
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_utils.settings.settings_loader import SettingsLoader
import urllib2
import unittest
import time
from urllib import urlencode

TEST_USER_ID = "test1"
TEST_USER_NAME = "test1"
TEST_USER_PIN = "test1"


class BaseTest(unittest.TestCase):
    """
    Requirements:

    1. A running TEST environment:
    /wikilife_ws/server-start.sh 7080 local

    2. Test users:
    test1 full active user
    test1000 to test9999 available user names
    """

    _settings = None

    def get_settings(self):
        """
        """
        if not self._settings:
            self._settings = SettingsLoader().load_settings("tests")
        return self._settings

    def get_logger(self):
        return MockLogger()

    def get_db_conn(self):
        db_user = None
        db_pass = None
        return DBConn(self.get_settings()["DB_SETTINGS"], db_user, db_pass)

    def get_dao_builder(self):
        return DAOBuilder(self.get_logger(), self.get_db_conn())

    def get_service_url(self, url_fragment):
        return "%s%s" % (self.get_settings()["WS_HOST"], url_fragment)

    def rest_get(self, url, params=None):
        """
        url: String
        params: Dict<String, String>
        """
        if params:
            url = self._get_url_with_qs(url, params)

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()
        
        return response_code, response_headers, response_body  

    def rest_post(self, url, body, params=None):
        """
        url: String
        body: String
        params: Dict<String, String>
        """
        if params:
            url = self._get_url_with_qs(url, params)

        request = urllib2.Request(url, body)
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()
        
        return response_code, response_headers, response_body  

    def rest_put(self, url, body, params=None):
        """
        url: String
        body: String
        params: Dict<String, String>
        """
        if params:
            url = self._get_url_with_qs(url, params)

        request = urllib2.Request(url, body)
        request.get_method = lambda: 'PUT'
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()
        
        return response_code, response_headers, response_body  

    def rest_delete(self, url, params=None):
        """
        url: String
        params: Dict<String, String>
        """
        if params:
            url = self._get_url_with_qs(url, params)

        request = urllib2.Request(url)
        request.get_method = lambda: 'DELETE'
        response = urllib2.urlopen(request)
        response_code = response.code
        response_headers = response.headers.dict
        response_body = response.read()
        
        return response_code, response_headers, response_body  

    def _get_url_with_qs(self, url, params):
        url = "%s?%s" %(url, urlencode(params))
        return url

    def get_test_user(self):
        test_user = self.get_user_mgr().get_user_by_id(TEST_USER_ID)

        if test_user == None:
            raise Exception("test user not exists")

        return test_user

    def get_test_device_id(self):
        return "wikilife_ws.tests.device"

    def wait_seconds(self, seconds, msg=""):
        print "sleeping %s sec %s..." % (seconds, msg)
        time.sleep(seconds)


class MockLogger(object):

    def info(self, message):
        print message

    def error(self, message):
        print message
