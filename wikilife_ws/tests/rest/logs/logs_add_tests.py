# coding=utf-8

from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest


class LogsAddTests(BaseTest):

    _test_user_id = None
    _test_oauth_token = None

    @classmethod
    def setUpClass(cls):
        cls._test_user_id = "A"
        cls._test_oauth_token = "abc"

    @classmethod
    def tearDownClass(cls):
        cls._test_user_id = None
        cls._test_oauth_token = None

    def test_a(self):
        print "test_a " + self._test_user_id 

    def test_b(self):
        print "test_b " + self._test_user_id 

'''
    def test_insert_log(self):
        user_id, nodes, text, days_offset
        log = self._get_test_log(user_id, nodes, text, days_offset)

        url = self.get_service_url("/4/meta/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)


@Route("/4/logs")
class LogCollectionHandler(BaseLogsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def post(self, user_id):
        """
        Submits one or more `Log`_ objects.

        Request::

            {
                "logs": "<a list of Log objects>"
            }

        Returns a list with the ids of the newly created log entries.
        """
        logs = JSONParser.to_collection(self.sanitize_raw_data(self.request.body))
        for log in logs:
            log["userId"] = user_id
        self.add_log_source(logs, self.request.headers)
        inserted_ids = self._log_srv.add_logs(logs)
        self.success(inserted_ids)




# coding=utf-8


TEST_USER_ID = "CKJG3L"


class LogsAddTests(BaseTest):
    #Requires a running TEST environment
    # /wikilife_sandbox/sh_utils/mongo/local_prc_dbs_util.sh
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    #TODO verify processors execution (requires posting different logs categories)

    test_user_id = None
    generic_stats_mgr = None


    def test_add_single_log(self):
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        #loggable_id = 296
        execute_time = "2013-01-05 19:15:30 -0300"

        #create test log
        logs = []
        log = self._get_sample_log(TEST_USER_ID, root_slug, nodes, execute_time, "t5")
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

    def _get_test_log(self, user_id, nodes, text="", days_offset=0):
        exec_date = DateUtils.get_datetime_local("America/Argentina/Buenos_Aires")
        exec_date = DateUtils.add_days(exec_date, days_offset)
        exec_date_str = DateFormatter.to_datetime(exec_date)

        return {
            "id": None,
            "origId": 0,
            "oper": "i",
            "source": "test",
            "userId": user_id,
            "start": exec_date_str,
            "end": exec_date_str,
            "text": text,
            "nodes": nodes
        }

'''