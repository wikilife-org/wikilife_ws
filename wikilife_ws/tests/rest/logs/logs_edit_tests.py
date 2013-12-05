# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_data.managers.stats.generic_stats_manager import GenericStatsManager
from wikilife_ws.rest.base_handler import STATUS_SUCCESS
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter

TEST_USER_ID = "CKJG3L"


class LogsEditTests(BaseTest):
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

    def test_edit_single_log(self):
        log_id, execute_time = self._add_single_log()

        #create test delete log
        logs = []
        value_upd = "120"
        log = self._get_sample_edit_log(log_id, TEST_USER_ID, value_upd, execute_time)
        logs.append(log)

        body = JSONParser.to_json(logs)
        raw_response = self.rest_post("http://localhost:7080/2/logs/edit", body)
        print raw_response
        response = JSONParser.to_collection(raw_response)

        print response
        assert response != None
        assert response["status"] == STATUS_SUCCESS

        #check write-only logs db
        log_dao = self.get_dao_builder().build_log_dao()
        edited_log_id = response["data"][0]
        found_log = log_dao.get_log_by_id(edited_log_id)
        assert found_log != None
        assert found_log["oper"] == "u"
        assert found_log["nodes"][0]["value"] == value_upd


    """ helpers """

    def _get_sample_edit_log(self, log_id, user_id, value_upd, execute_time):
        return {
            'pk': log_id, 
            'model': 'LogEntry', 
            'fields': {'status': 1, 
                       'user_id': user_id, 
                       'text': '', 
                       'execute_time': execute_time, 
                       'original_entry': 0, 
                       'root_slug': 'exercise', 
                       'nodes': [{'node_id': 298, 'value': value_upd}]
                }
            }

    def _add_single_log(self):
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        current_date_local = DateUtils.get_datetime_local("America/Argentina/Buenos_Aires")
        execute_time = DateFormatter.to_datetime(current_date_local)

        #create test log
        logs = []
        log = self._get_sample_log(TEST_USER_ID, root_slug, nodes, execute_time)
        logs.append(log)

        body = JSONParser.to_json(logs)
        raw_response = self.rest_post("http://localhost:7080/2/logs/add", body)
        print raw_response
        response = JSONParser.to_collection(raw_response)

        added_log_id = response["data"][0]
        return added_log_id, execute_time
        
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
