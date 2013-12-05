# coding=utf-8

from wikilife_log_service.utils.log_service_builder import LogServiceBuilder
from wikilife_user_service.utils.user_service_builder import UserServiceBuilder
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest


TEST_HUMAN_INTERNAL_USER_NAME = "TEST_USER_4"


class UsersSettingsTests(BaseTest):

    _timeline_mgr = None
    _log_mgr = None
    _final_log_mgr = None
    _user_mgr = None
    _profile_mgr = None
    _log_srv = None
    _account_srv = None
    _human_user_id = None

    def setUp(self):
        mgr_bldr = self.get_manager_builder()
        user_srv_bldr = UserServiceBuilder(self.get_settings(), self.get_logger(), mgr_bldr)
        log_srv_bldr = LogServiceBuilder(self.get_settings(), self.get_logger(), mgr_bldr)
        self._timeline_mgr = mgr_bldr.build_timeline_manager()
        self._user_mgr = mgr_bldr.build_user_manager()
        self._log_mgr = mgr_bldr.build_log_manager()
        self._final_log_mgr = mgr_bldr.build_final_log_manager()
        self._profile_mgr = mgr_bldr.build_profile_manager()
        self._log_srv = log_srv_bldr.build_log_service(user_srv_bldr.build_user_service())
        self._account_srv = user_srv_bldr.build_account_service(self._log_srv)

    def tearDown(self):
        self._delete_human_user(self._human_user_id)
        
    def test_delete_log(self):
        """
        create test user
        wait prcs
        check timeline
        
        add excercise log
        wait prcs
        check timeline
        
        delete log
        wait prcs
        check timeline
        """
        self._human_user_id = self._create_human_user(TEST_HUMAN_INTERNAL_USER_NAME)
        print self._human_user_id
        profile_logs_count = self._count_user_logs(self._human_user_id)
        self.wait_seconds(10, "for initial profile logs to be processed ")
        assert self._has_full_functional_user(self._human_user_id)
        assert self._count_timeline_items(self._human_user_id) == profile_logs_count

        log_id = self._add_excercise_log(self._human_user_id)
        self.wait_seconds(5, "for new log to be processed ")
        assert self._count_timeline_items(self._human_user_id) == profile_logs_count+1

        self._delete_log(self._human_user_id, log_id)
        self.wait_seconds(5, "for log to be deleted ")
        assert self._count_timeline_items(self._human_user_id) == profile_logs_count
        assert self._count_user_final_logs(self._human_user_id) == profile_logs_count
        
        self._delete_human_user(self._human_user_id)

    """ helpers """

    def _create_human_user(self, user_name):
        try:
            user_id = self._user_mgr.get_user_by_user_name(user_name)["user_id"]
            self._delete_human_user(user_id)
        except: pass
        
        account_dto = {}
        account_dto["timezone"] = "America/Argentina/Buenos_Aires"
        account_dto["user_name"] = user_name
        account_dto["pin"] = "1234"
        created_user = self._account_srv.create_account(account_dto)
        return created_user["user_id"]
    
    def _delete_human_user(self, user_id):
        try:
            self._account_srv.delete_account(user_id)
        except Exception, e:
            print "_delete_human_user: %s" %e

    def _add_excercise_log(self, user_id):
        logs = []
        logs.append(self._create_log(user_id, "human 1", "exercise", [{"node_id": 298, "value": "10"}], "timeline_delete_tests.human", "2012-08-01 12:00:00 +0000"))
        inserted_ids = self._log_srv.add_logs(logs)
        return inserted_ids[0]

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
        return self._log_mgr._collection.find({"fields.user_id": user_id}).count()

    def _count_user_final_logs(self, user_id):
        return self._final_log_mgr.get_final_logs_by_user(user_id).count()

    def _has_full_functional_user(self, user_id):
        db_users = self.get_db_conn().get_conn_users()

        if db_users.users.find({"user_id": user_id}).count() == 0:
            return False

        if self._profile_mgr.get_profile_by_user_id(user_id) == None:
            return False

        if self._count_user_logs(user_id) == 0:
            return False
        
        if self._count_user_final_logs(user_id) == 0:
            return False

        #TODO may check other collections

        return True

    def _delete_log(self, user_id, log_id):
        url = self.get_service_url("/1/logs/delete.json")
        
        #[{'fields': {'user_id': 'X6Q4WT'}, 'pk': 15199}]
        
        log = {}
        log["pk"] = log_id
        log["fields"] = {}
        log["fields"]["user_id"] = user_id
            
        try:
            body = JSONParser.to_json([log])
            response = self.rest_post(url, body)
            print "response: %s" %response 

        except Exception, e:
            print "_delete_log: %s" %e
            assert False

        assert response == "OK"
