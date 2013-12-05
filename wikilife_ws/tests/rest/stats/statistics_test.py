# coding=utf-8

from wikilife_ws.tests.base_ws_test import BaseWSTest
from wikilife_utils.json_parser import JSONParser
from wikilife_data.managers.logs.log_manager import LogManager
from wikilife_data.managers.stats.generic_stats_manager import GenericStatsManager


class StatisticsTests(BaseWSTest):
    #Requires a running TEST environment
    # /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_query_50(self):

        #invoke ws
        params = {"food_ids": [26164, ], "serving_sizes": [2.0]}
        try:
            raw_response = self.rest_get("http://localhost:7080/1/query/50.json", params)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
