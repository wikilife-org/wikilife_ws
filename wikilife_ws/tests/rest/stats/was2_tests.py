# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter

TEST_USER_ID = "TEST"
TEST_OAUTH_TOKEN = "testusertoken"
HOST = "http://localhost:7080"

class Was2Tests(BaseTest):
    #Requires a running TEST environment
    # Neo4j 
    # /wikilife_processors/server-start.sh local
    # /wikilife_ws/server-start.sh 7080 local

    def test_add_numeric(self):
        nodes = [{"nodeId": 41300, "metricId": 41302, "value": 5 }]
        text = "test log"
        days_offset = 0

        #create test log
        logs = []
        log = self._get_test_log(TEST_USER_ID, nodes, text, days_offset)
        logs.append(log)

        #invoke ws
        try:
            body = JSONParser.to_json(logs)
            params = {"oauth_token": TEST_OAUTH_TOKEN}
            response_code, response_headers, response_body = self.rest_post(HOST+"/4/logs", body, params)
            print response_code, response_headers, response_body
            response = JSONParser.to_collection(response_body)
        except Exception, e:
            print e
            assert False

        print response
        assert response != None

    def NO_test_add_options(self):
        nodes = [{"nodeId": 41300, "metricId": 8, "value": "Outdoors" }]
        text = "test log"
        days_offset = 0

        #create test log
        logs = []
        log = self._get_test_log(TEST_USER_ID, nodes, text, days_offset)
        logs.append(log)

        #invoke ws
        try:
            body = JSONParser.to_json(logs)
            params = {"oauth_token": TEST_OAUTH_TOKEN}
            response_code, response_headers, response_body = self.rest_post(HOST+"/4/logs", body, params)
            print response_code, response_headers, response_body
            response = JSONParser.to_collection(response_body)
        except Exception, e:
            print e
            assert False

        print response
        assert response != None

    def NO_test_read_numeric(self):
        #invoke ws
        try:
            params = {}
            params["node_id"] = 41300
            params["metric_id"] = 413002
            params["from"] = "2013-08-01"
            params["to"] = "2013-08-22"

            response_code, response_headers, response_body = self.rest_get(HOST+"/4/was", params)
            print response_code, response_headers, response_body
            response = JSONParser.to_collection(response_body)
        except Exception, e:
            print e
            assert False

        print response
        assert response != None

    def test_read_user_numeric(self):
        pass
   
    
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


    """
        try:
            http_client = HTTPClient()
            http_client.fetch(HTTPRequest(url="http://"+self.request.host+"/4/account", method='POST', body=self.request.body))
            raise Exception()
        except Exception, e:
            self._logger.exception(e)
        finally:
            http_client.close()
    """