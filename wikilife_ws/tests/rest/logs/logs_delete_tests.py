# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_data.managers.stats.generic_stats_manager import GenericStatsManager
from wikilife_ws.rest.base_handler import STATUS_SUCCESS

TEST_USER_ID = "CKJG3L"


class LogsDeleteTests(BaseTest):
    #Requires a running TEST environment
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    test_user_id = None
    generic_stats_mgr = None

    def NO_setUp(self):
        self.generic_stats_mgr = GenericStatsManager(self.get_logger(), self.get_stats_db())
        self.generic_stats_mgr.delete_weekly_stats_by_user_id(self.test_user_id)

    def NO_tearDown(self):
        self.generic_stats_mgr.delete_weekly_stats_by_user_id(self.test_user_id)

    def test_delete_single_log(self):
        log_id = self._add_single_log()
        
        #create test delete log
        logs = []
        log = self._get_sample_delete_log(log_id, TEST_USER_ID)
        logs.append(log)

        body = JSONParser.to_json(logs)
        raw_response = self.rest_post("http://localhost:7080/2/logs/delete", body)
        print raw_response
        response = JSONParser.to_collection(raw_response)

        print response
        assert response != None
        assert response["status"] == STATUS_SUCCESS


    """ helpers """

    def _get_sample_delete_log(self, log_id, user_id):
        return {'fields': {'user_id': user_id}, 'pk': log_id}

    def _add_single_log(self):
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        execute_time = "2012-02-02 19:15:43 -0300"

        #create test log
        logs = []
        log = self._get_sample_log(TEST_USER_ID, root_slug, nodes, execute_time)
        logs.append(log)

        body = JSONParser.to_json(logs)
        raw_response = self.rest_post("http://localhost:7080/2/logs/add", body)
        print raw_response
        response = JSONParser.to_collection(raw_response)

        added_log_id = response["data"][0]
        return added_log_id
        
    def _get_sample_log(self, user_id, root_slug, nodes, execute_time, text=""):
        return {
            "pk": 0,
            "model": "LogEntry",
            "fields": {
                "status": 1,
                "execute_time": execute_time,
                "text": text,
                "original_entry": 0,
                "root_slug": root_slug,
                "user_id": user_id,
                "nodes": nodes
            }
        }
