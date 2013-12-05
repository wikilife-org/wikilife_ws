# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest


class MetaTests(BaseTest):

    def test_meta_node_by_id(self):
        node_id = 1
        expected = {
            "id": node_id,
            "origId": 1,
            "name": "Life Variable",
            "otherNames": "Wikilife",
            "type": "MetaNode"
        }

        url = self.get_service_url("/4/meta/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def _test_meta_node_by_id_not_existing_node(self):
        node_id = 0
        url = self.get_service_url("/4/meta/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)

        self.assertEquals(response_code, 400)

    def test_meta_node_with_metrics(self):
        node_id = 6
        expected = {       
            "id": node_id,
            "origId": 49,
            "name": "Exercise",
            "otherNames": "",
            "type": "MetaNode",
            "metrics": [
                {
                    "name": "With?-Value Node",
                    "default": 3,
                    "origId": 432,
                    "id": 9,
                    "type": "TextMetricNode",
                    "options": "Personal Trainner,Coach,Class Mates,Alone,Life Partner,Boyfriend,Girlfriend,Pet,Family,Friends,Coworker"
                },
                {
                    "name": "Where?-Value Node",
                    "default": 0,
                    "origId": 434,
                    "id": 8,
                    "type": "TextMetricNode",
                    "options": "Home,Outdoors,Country Club,Gym"
                },
                {
                    "name": "How Do You Feel?-Value Node",
                    "default": 5,
                    "origId": 436,
                    "id": 7,
                    "type": "TextMetricNode",
                    "options": "Energetic,Happy,Sad,Moody,Exhausted,Well Enough,Tired But Happy,Still Stressed,Unhappy"
                }
            ]
        }

        url = self.get_service_url("/4/meta/withmetrics/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def test_meta_node_by_orig_id(self):
        orig_id = 1
        expected = {
            "id": 1,
            "origId": orig_id,
            "name": "Life Variable",
            "otherNames": "Wikilife",
            "type": "MetaNode"
        }

        url = self.get_service_url("/4/meta/origid/%s" %orig_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def test_meta_node_parents(self):
        node_id = 6
        expected = [{
            "id": 1,
            "origId": 1,
            "name": "Life Variable",
            "otherNames": "Wikilife",
            "type": "MetaNode"
        }]

        url = self.get_service_url("/4/meta/parents/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertListEqual(expected, result)
    
    def test_meta_node_ancestors(self):
        node_id = 10
        expected = [
            {
                "name": "Exercise",
                "parentIds": [
                    1
                ],
                "origId": 49,
                "otherNames": "",
                "type": "MetaNode",
                "id": 6
            },
            {
                "name": "Life Variable",
                "parentIds": [ ],
                "origId": 1,
                "otherNames": "Wikilife",
                "type": "MetaNode",
                "id": 1
            }
        ]

        url = self.get_service_url("/4/meta/ancestors/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertListEqual(expected, result)
    
    def test_meta_node_children(self):
        node_id = 1
        expected = {
            "pageIndex": 0,
            "pageSize": 25,
            "pageCount": 1,
            "items": [
                {
                    "otherNames": "",
                    "origId": 407267,
                    "type": "MetaNode",
                    "id": 2,
                    "name": "Education"
                },
                {
                    "otherNames": "",
                    "origId": 49,
                    "type": "MetaNode",
                    "id": 6,
                    "name": "Exercise"
                },
                {
                    "otherNames": "",
                    "origId": 976,
                    "type": "MetaNode",
                    "id": 13,
                    "name": "Health"
                },
                {
                    "otherNames": "",
                    "origId": 526,
                    "type": "MetaNode",
                    "id": 313,
                    "name": "Journal"
                },
                {
                    "otherNames": "",
                    "origId": 461,
                    "type": "MetaNode",
                    "id": 314,
                    "name": "Leisure"
                },
                {
                    "otherNames": "",
                    "origId": 661,
                    "type": "MetaNode",
                    "id": 325,
                    "name": "Milestones"
                },
                {
                    "otherNames": "",
                    "origId": 400006,
                    "type": "MetaNode",
                    "id": 338,
                    "name": "Mood"
                },
                {
                    "otherNames": "",
                    "origId": 509,
                    "type": "MetaNode",
                    "id": 339,
                    "name": "Nutrition"
                },
                {
                    "otherNames": "",
                    "origId": 435500,
                    "type": "MetaNode",
                    "id": 347,
                    "name": "Personal Care"
                },
                {
                    "otherNames": "",
                    "origId": 2,
                    "type": "MetaNode",
                    "id": 349,
                    "name": "Physiological"
                },
                {
                    "otherNames": "",
                    "origId": 1137,
                    "type": "MetaNode",
                    "id": 350,
                    "name": "Profile"
                },
                {
                    "otherNames": "",
                    "origId": 527,
                    "type": "MetaNode",
                    "id": 355,
                    "name": "Psychological"
                },
                {
                    "otherNames": "",
                    "origId": 491,
                    "type": "MetaNode",
                    "id": 360,
                    "name": "Sex"
                },
                {
                    "otherNames": "",
                    "origId": 317606,
                    "type": "MetaNode",
                    "id": 363,
                    "name": "Spirituality"
                },
                {
                    "otherNames": "",
                    "origId": 437,
                    "type": "MetaNode",
                    "id": 364,
                    "name": "Travel"
                },
                {
                    "otherNames": "",
                    "origId": 453,
                    "type": "MetaNode",
                    "id": 366,
                    "name": "Work"
                }
            ]
        }

        url = self.get_service_url("/4/meta/children/%s" %node_id)
        response_code, response_headers, response_body = self.rest_get(url)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)
