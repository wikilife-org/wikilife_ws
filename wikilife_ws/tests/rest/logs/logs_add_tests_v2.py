# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_data.managers.stats.generic_stats_manager import GenericStatsManager
from wikilife_ws.rest.base_handler import STATUS_SUCCESS

TEST_USER_ID = "CKJG3L"


class LogsAddTests(BaseTest):
    #Requires a running TEST environment
    # /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    #TODO verify processors execution (requires posting different logs categories)

    test_user_id = None
    generic_stats_mgr = None

    def NO_setUp(self):
        self.generic_stats_mgr = GenericStatsManager(self.get_logger(), self.get_stats_db())
        self.generic_stats_mgr.delete_weekly_stats_by_user_id(self.test_user_id)

    def NO_tearDown(self):
        self.generic_stats_mgr.delete_weekly_stats_by_user_id(self.test_user_id)

    def test_add_single_log(self):
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        #loggable_id = 296
        execute_time = "2013-01-05 19:15:30 -0300"

        #create test log
        logs = []
        log = self._get_sample_log(TEST_USER_ID, root_slug, nodes, execute_time, "t4")
        logs.append(log)

        #invoke ws
        try:
            body = JSONParser.to_json(logs)
            raw_response = self.rest_post("http://localhost:7080/2/logs/add", body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        print response
        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert isinstance(response["data"], list)
        assert len(response["data"]) == 1

        #check write-only logs db
        log_mgr = self.get_dao_builder().build_log_dao()
        added_log_id = response["data"][0]
        found_log = log_mgr.get_log_by_id(added_log_id)
        assert found_log != None
        assert found_log["source"].startswith("client.other")
        assert found_log["oper"] == "i"

        
    """ helpers """

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
