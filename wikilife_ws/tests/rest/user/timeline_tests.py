# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import STATUS_SUCCESS
from wikilife_ws.tests.base_test import BaseTest, TEST_USER_ID
import time


class TimelineTests(BaseTest):

    def test_sync_user_timeline(self):
        pass

    def NO_test_timeline_workflow(self):
        user = self._get_test_user()
        log = self._add_test_log()

        #question = self.get_question_mgr().get_question_by_id(179)
        #answer_value = "frequently"
        question = self.get_question_mgr().get_question_by_id(195)
        answer_value = "Sometimes"

        answer, answer_log = self._add_test_answer(user, question, answer_value)
        date_str = self._get_log_date_str(log)

        expected_response = {
            "status": STATUS_SUCCESS,
            "message": "Get Stream for User API",
            "data": [
                {"date": date_str, "logs": [
                    {"id": log["pk"], "info": {"type": "log"}, "time": log["fields"]["execute_time"], "category": log["fields"]["root_slug"], "text": log["fields"]["text"], "nodes": log["fields"]["nodes"]},
                    {"id": answer_log["pk"], "info": {"type": "answer", "question_id": question["pk"], "answer_id": answer["answer_id"]}, "time": answer_log["fields"]["execute_time"], "category": answer_log["fields"]["root_slug"], "text": answer_log["fields"]["text"], "nodes": answer_log["fields"]["nodes"]}
                ]}
            ]
        }

        url = self.get_service_url("/2/logs/user_timeline.json")
        params = {"user_id": user["user_id"]}

        #wait for async processors to run
        print "sleeping 2 sec to wait for async processors to run ..."
        time.sleep(2)

        #invoke ws
        try:
            raw_response = self.rest_get(url, params)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == expected_response["status"]
        assert response["message"] == expected_response["message"]
        assert len(response["data"]) == len(expected_response["data"])

        day = response["data"][0]
        expected_day = expected_response["data"][0]
        assert day["date"] == expected_day["date"]
        assert len(day["logs"]) == len(expected_day["logs"])

        day_log = day["logs"][0]
        expected_day_log = expected_day["logs"][0]
        assert day_log["id"] == expected_day_log["id"]
        assert day_log["info"] == expected_day_log["info"]
        assert day_log["time"] == expected_day_log["time"]
        assert day_log["category"] == expected_day_log["category"]
        assert day_log["text"] == expected_day_log["text"]
        #assert day_log["nodes"] == expected_day_log["nodes"]

        day_answer_log = day["logs"][1]
        expected_day_answer_log = expected_day["logs"][1]
        assert day_answer_log["id"] == expected_day_answer_log["id"]
        assert day_answer_log["info"] == expected_day_answer_log["info"]
        assert day_answer_log["time"] == expected_day_answer_log["time"]
        assert day_answer_log["category"] == expected_day_answer_log["category"]
        assert day_answer_log["text"] == expected_day_answer_log["text"]
        #assert day_answer_log["nodes"] == expected_day_answer_log["nodes"]

    '''
    def NO_test_get_user_timeline(self):
        """
        Sample API-2 request/response:

        http://qaapi.wikilife.org/2/logs/user_timeline.json?user_id=8MPLXE&roots=healthcare,nutrition

        RESP:
        {"status": "OK", "message": "Get Stream for User API", "data": [{"date": "2012-02-22", "logs": [{"category": "nutrition", "text": "Large Hamburger  0.8 sandwich", "nodes": [{"node_id": 74004, "value": 0.80}], "id": 206900, "time": "2012-02-22 22:47:03 +0000"}]}, {"date": "2012-02-15", "logs": [{"category": "healthcare", "text": "I do not wash my hands before eating?", "nodes": [{"node_id": 251374.00, "value": "No"}], "id": 206797, "time": "2012-02-15 18:47:42 +0000"}]}, {"date": "2012-02-13", "logs": [{"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 206751, "time": "2012-02-13 23:53:09 +0000"}, {"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 206749, "time": "2012-02-13 14:58:27 +0000"}]}, {"date": "2012-02-12", "logs": [{"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 206754, "time": "2012-02-12 23:53:55 +0000"}]}, {"date": "2012-02-02", "logs": [{"category": "nutrition", "text": "Large Hamburger  1.0 sandwich, With? Friends", "nodes": [{"node_id": 74004, "value": 1.00}, {"node_id": 517, "value": "Friends"}], "id": 206282, "time": "2012-02-02 22:16:56 +0000"}]}, {"date": "2012-01-26", "logs": [{"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 205902, "time": "2012-01-26 13:53:52 +0000"}]}, {"date": "2012-01-23", "logs": [{"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 205873, "time": "2012-01-23 17:59:44 +0000"}]}, {"date": "2011-12-14", "logs": [{"category": "nutrition", "text": "Water  1.0 cup (8 fl oz)", "nodes": [{"node_id": 2229, "value": 1.00}], "id": 205620, "time": "2011-12-14 20:11:52 +0000"}, {"category": "nutrition", "text": "Coconut Water  1.0 cup", "nodes": [{"node_id": 133203, "value": 1.00}], "id": 205619, "time": "2011-12-14 20:11:06 +0000"}]}, {"date": "2011-12-05", "logs": [{"category": "healthcare", "text": "I have not practiced homeopathy", "nodes": [{"node_id": 241508, "value": "No"}], "id": 205063, "time": "2011-12-05 12:08:10 +0000"}, {"category": "healthcare", "text": "I occasionally use sunscreen", "nodes": [{"node_id": 241557, "value": "Occasionally"}], "id": 205062, "time": "2011-12-05 12:07:59 +0000"}]}, {"date": "2011-11-22", "logs": [{"category": "nutrition", "text": "Beef Top Round (Trimmed to 1/8\" Fat)  1.0 oz", "nodes": [{"node_id": 214305, "value": 1.00}], "id": 203192, "time": "2011-11-22 14:55:41 +0000"}]}, {"date": "2011-11-17", "logs": [{"category": "nutrition", "text": "Water  1.0 cup (8 fl oz)", "nodes": [{"node_id": 2229, "value": 1.00}], "id": 178473, "time": "2011-11-17 15:45:24 +0000"}]}, {"date": "2011-11-08", "logs": [{"category": "nutrition", "text": "Hamburger on Bun  1.0 hamburger", "nodes": [{"node_id": 183654, "value": 1.00}], "id": 131856, "time": "2011-11-08 18:34:59 +0000"}, {"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 131702, "time": "2011-11-08 18:04:12 +0000"}]}, {"date": "2011-11-02", "logs": [{"category": "nutrition", "text": "Raisins  1.0 cup", "nodes": [{"node_id": 131376, "value": 1.00}], "id": 100785, "time": "2011-11-02 21:27:25 +0000"}, {"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 99689, "time": "2011-11-02 17:41:26 +0000"}, {"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 99543, "time": "2011-11-02 17:35:02 +0000"}, {"category": "nutrition", "text": "Large Hamburger  1.0 sandwich", "nodes": [{"node_id": 74004, "value": 1.00}], "id": 99542, "time": "2011-11-02 17:29:10 +0000"}]}]}
        """

        categories = "healthcare,nutrition"
        url = self.get_service_url("/2/logs/user_timeline.json")
        params = {"user_id": TEST_USER_ID, "roots": categories}

        #invoke ws
        try:
            raw_response = self.rest_get(url, params)
            print raw_response
            response = JSONParser.to_collection(raw_response)
        except Exception, e:
            print e
            assert False

        assert response != None
        assert response["status"] == STATUS_SUCCESS
        assert response["message"] == "Get Stream for User API"
        assert response["data"] != None
    '''

    """ helpers """

    def _add_test_log(self):
        root_slug = "exercise"
        nodes = [{"node_id": 298, "value": "60"}]
        execute_time = "2012-03-19 19:15:43 -0300"
        logs = []
        log = self._get_sample_log(TEST_USER_ID, root_slug, nodes, execute_time)
        logs.append(log)
        body = JSONParser.to_json(logs)
        url = self.get_service_url("/2/logs/add.json")
        raw_response = self.rest_post(url, body)
        response = JSONParser.to_collection(raw_response)
        added_log_id = response["data"][0]
        found_log = self.get_log_mgr().get_log_by_id(added_log_id)

        return found_log

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

    def _add_test_answer(self, user, question, answer_value):

        dto = {
            "answer": {
                "execute_time": "2012-03-19 12:13:01 -0300",
                "answer_value": answer_value,
                "question_id": question["pk"],
                "answer_id": 0
            },
            "user_id": user["user_id"],
            "answer_type": "1"
        }

        body = JSONParser.to_json(dto)
        url = self.get_service_url("/2/questions/answer/add.json")
        raw_response = self.rest_post(url, body)
        response = JSONParser.to_collection(raw_response)
        answer = response["data"]["answer"]
        log_id = answer["log_id"]
        answer_log = self.get_log_mgr().get_log_by_id(log_id)

        return answer, answer_log

    def _get_log_date_str(self, log):
        date_str = log["fields"]["execute_time"][:10]
        return date_str
