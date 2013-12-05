# coding=utf-8

from wikilife_ws.tests.base_ws_test import BaseWSTest
from wikilife_utils.json_parser import JSONParser


class LogsTests(BaseWSTest):
    #Requires a running TEST environment
    # /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    #TODO verify processors execution (requires posting different logs categories)

    test_user_id = None
    generic_stats_mgr = None

    def setUp(self):
        self.test_user_id = "8MPLXE"

    def tearDown(self):
        pass

    def test_add_single_log(self):
        user_id = self.test_user_id
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        loggable_id = 296
        execute_time = "2012-02-02 19:15:43 -0300"

        #create test log
        logs = []
        log = self._get_sample_log(user_id, root_slug, nodes, execute_time)
        logs.append(log)

        #invoke ws
        try:
            body = JSONParser.to_json(logs)
            #raw_response = self.rest_post("http://localhost:7080/2/logs/add", body)
            raw_response = self.rest_post("http://ec2-50-16-69-82.compute-1.amazonaws.com/2/logs/add", body)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == "success"
        assert isinstance(response["data"], list)
        assert len(response["data"]) == 1

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
