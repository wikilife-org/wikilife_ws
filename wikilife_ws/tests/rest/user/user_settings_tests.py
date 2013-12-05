# coding=utf-8

from wikilife_log_service.utils.log_service_builder import LogServiceBuilder
from wikilife_user_service.utils.user_service_builder import UserServiceBuilder
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import STATUS_SUCCESS
from wikilife_ws.tests.base_test import BaseTest
import time


SRV_ROUTE_TPL = "/2/settings/twitter/%s.json" 
TEST_HUMAN_INTERNAL_USER_NAME = "TEST_HUMAN"


class UsersSettingsTests(BaseTest):

    _timeline_mgr = None
    _log_mgr = None
    _user_mgr = None
    _profile_mgr = None
    _log_srv = None
    _account_srv = None
    _twitter_user_srv = None
    _human_user_id = None

    def setUp(self):
        mgr_bldr = self.get_manager_builder()
        user_srv_bldr = UserServiceBuilder(self.get_settings(), self.get_logger(), mgr_bldr)
        log_srv_bldr = LogServiceBuilder(self.get_settings(), self.get_logger(), mgr_bldr)
        self._timeline_mgr = mgr_bldr.build_timeline_manager()
        self._user_mgr = mgr_bldr.build_user_manager()
        self._log_mgr = mgr_bldr.build_log_manager()
        self._profile_mgr = mgr_bldr.build_profile_manager()
        self._log_srv = log_srv_bldr.build_log_service(user_srv_bldr.build_user_service())
        self._account_srv = user_srv_bldr.build_account_service(self._log_srv)
        self._twitter_user_srv = user_srv_bldr.build_twitter_user_service(self._log_srv)
        self._human_user_id = self._create_human_user(TEST_HUMAN_INTERNAL_USER_NAME)

    def tearDown(self):
        self._delete_human_user(self._human_user_id)
        self._timeline_mgr = None
        self._log_mgr = None
        self._user_mgr = None
        self._profile_mgr = None
        self._log_srv = None
        self._account_srv = None
        self._twitter_user_srv = None

    def test_set_twitter_settings(self):
        """
        Sample API-1 request/response:
        @Route('/2/settings/twitter/(?P<user_id>[-\w]+).json')

        REQUEST: 
        {"roots":[""],"active":True,"access_token_secret":"","access_token_key":""}       

        RESPONSE:
        {"status": "OK", "message": null, data: null}
        """
        
        """
        create twitter user
        add twitter logs
        
        create internal user
        add logs
        
        wait for prcs 
        
        verify timelines
        
        merge users
        
        assert twitter internal user is gone
        
        assert internal user has both users logs
        assert internal user timeline is the sum of the two old timelines
        """

        print self._human_user_id
        print self._crawler_user_id

        human_logs_count = self._add_human_logs(self._human_user_id)
        crawler_logs_count = self._add_crawler_logs(self._crawler_user_id)
        total_logs = human_logs_count + crawler_logs_count
        
        self._wait_seconds(2)

        assert self._count_timeline_items(self._human_user_id) == human_logs_count
        assert self._count_timeline_items(self._crawler_user_id) == crawler_logs_count

        twitter_settings = self._create_twitter_settings(TEST_TWITTER_USER_ID)
        self._post_twitter_settings(self._human_user_id, twitter_settings)

        self._wait_seconds(5)

        assert self._has_full_functional_user(self._human_user_id)
        assert self._has_no_trace_from_user(self._crawler_user_id)
        assert self._count_user_logs(self._human_user_id) == total_logs
        assert self._count_timeline_items(self._human_user_id) == total_logs

    '''
    def __test_post_twitter_settings_basic(self):
        """
        Sample API-1 request/response:

        @Route('/2/settings/twitter/(?P<user_id>[-\w]+).json')

        POST: 
        {"roots":[""],"active":True,"access_token_secret":"","access_token_key":""}       

        RESP:
        {"status": "OK", "message": null, data: null}
        """
        TEST_USER_INTERNAL_ID = "X278Q9"
        TEST_USER_TWITTER_ID = "7071151"

        url = self.get_service_url("/2/settings/twitter/%s.json" %TEST_USER_INTERNAL_ID) 
        #twitter_settings = {"roots": [""],"active": True, "access_token_secret": ""}
        #twitter_settings["access_token_key"] = "%s-sarasa" %TEST_USER_TWITTER_ID
        twitter_settings = self._get_twitter_settings(TEST_USER_TWITTER_ID)

        #invoke ws
        try:
            body = JSONParser.to_json(twitter_settings)
            raw_response = self.rest_post(url, body)
            print raw_response 
            response = JSONParser.to_collection(raw_response)

        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == None
        assert response["data"] == None
    '''

    """ helpers """

    def _create_human_user(self, user_name):
        try:
            user_id = self._user_mgr.get_user_by_user_name(user_name)["user_id"]
            self._delete_human_user(user_id)
        except: pass
        
        account_dto = {}
        account_dto["user_name"] = user_name
        account_dto["timezone"] = "America/Argentina/Buenos_Aires"
        account_dto["pin"] = "1234"
        created_user = self._account_srv.create_account(account_dto)
        return created_user["user_id"]
    
    def _create_crawler_user(self, twitter_user_id):
        created_user = self._twitter_user_srv.create_twitter_user(twitter_user_id)
        return created_user["internal_id"]

    def _delete_human_user(self, user_id):
        self._account_srv.delete_account(user_id)

    def _delete_crawler_user(self, user_id):
        self._account_srv.delete_account(user_id)
        #TODO logs, pre processed, etc

    def _add_human_logs(self, user_id):
        logs = []
        logs.append(self._create_log(user_id, "human 1", "exercise", [{"node_id": 298, "value": "1"}], "user_settings_tests.human", "2012-06-01 12:00:00 +0000"))
        logs.append(self._create_log(user_id, "human 2", "exercise", [{"node_id": 298, "value": "2"}], "user_settings_tests.human", "2012-06-02 12:00:00 +0000"))
        self._log_srv.add_logs(logs)
        return self._count_user_logs(user_id)

    def _add_crawler_logs(self, user_id):
        logs = []
        logs.append(self._create_log(user_id, "crawler 3", "exercise", [{"node_id": 298, "value": "3"}], "user_settings_tests.crawler", "2012-06-01 12:30:00 +0000"))
        logs.append(self._create_log(user_id, "crawler 4", "exercise", [{"node_id": 298, "value": "4"}], "user_settings_tests.crawler", "2012-06-02 12:30:00 +0000"))
        logs.append(self._create_log(user_id, "crawler 5", "exercise", [{"node_id": 298, "value": "5"}], "user_settings_tests.crawler", "2012-06-03 12:30:00 +0000"))
        self._log_srv.add_logs(logs)
        return self._count_user_logs(user_id)

    def _create_log(self, user_id, text, root_slug, nodes, source, execute_time):
        log = {
            "pk": 0,
            "model": "LogEntry",
            "fields": {
                "status": 1,
                "execute_time": execute_time,
                "text": text,
                "original_entry": 0,
                "root_slug": root_slug,
                "user_id": user_id,
                "source" : source,
                "nodes": nodes
            }
        }
        
        return log

    def _count_timeline_items(self, user_id):
        count = 0

        for day in self._timeline_mgr._collection.find({"user_id": user_id}):
            count += len(day["logs"])

        return count

    def _count_user_logs(self, user_id):
        #return self._log_mgr._collection.find({"fields.user_id": user_id,  "fields.root_slug": {"$ne": "profile"}}).count()
        return self._log_mgr._collection.find({"fields.user_id": user_id}).count()

    def _has_full_functional_user(self, user_id):
        db_users = self.get_db_conn().get_conn_users()

        if db_users.users.find({"user_id": user_id}).count() == 0:
            return False

        if self._profile_mgr.get_profile_by_user_id(user_id) == None:
            return False

        #TODO may check other collections

        return True

    def _has_no_trace_from_user(self, user_id):
        db_users = self.get_db_conn().get_conn_users()

        if db_users.users.find({"user_id": user_id}).count() > 0:
            return False

        if db_users.twitter_users.find({"internal_id": user_id}).count() > 0:
            return False

        if db_users.twitter_settings.find({"user_id": user_id}).count() > 0:
            return False

        if db_users.user_recovery_information.find({"user_id": user_id}).count() > 0:
            return False

        if db_users.user_token.find({"user_id": user_id}).count() > 0:
            return False

        if self._profile_mgr.get_profile_by_user_id(user_id) != None:
            return False

        if self._count_user_logs(user_id) > 0:
            return False

        if self._count_timeline_items(user_id) > 0:
            return False

        #TODO may check other preprocesed collections

        return True

    def _create_twitter_settings(self, twitter_id):
        twitter_settings = {"roots": [""],"active": True, "access_token_secret": ""}
        twitter_settings["access_token_key"] = "%s-sarasa" %twitter_id
        return twitter_settings
    
    def _post_twitter_settings(self, internal_user_id, twitter_settings):
        url = self.get_service_url(SRV_ROUTE_TPL %internal_user_id)

        try:
            body = JSONParser.to_json(twitter_settings)
            raw_response = self.rest_post(url, body)
            print raw_response 
            response = JSONParser.to_collection(raw_response)

        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == None
        assert response["data"] == None

    def _wait_seconds(self, seconds):
        #wait for async processors to run
        print "sleeping %s sec to wait for async processors to run ..." %seconds
        time.sleep(seconds)
