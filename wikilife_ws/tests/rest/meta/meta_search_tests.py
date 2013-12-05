# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.tests.base_test import BaseTest


class MetaSearchTests(BaseTest):

    def test_meta_search_by_name(self):
        expected = {
            "items": [
                {
                    "name": "Lower Abdominal Pain",
                    "parentIds": [
                        15
                    ],
                    "origId": 253273,
                    "otherNames": "Lower abdominal pain, R10.3",
                    "type": "MetaNode",
                    "id": 1251
                }
            ],
            "pageIndex": 0,
            "pageSize": 25,
            "pageCount": 1
        }

        params = {"name": "Lower Abdominal Pain"}
        url = self.get_service_url("/4/meta/search/")
        response_code, response_headers, response_body = self.rest_get(url, params)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def test_meta_search_case_insensitive(self):
        expected = {
            "items": [
                {
                    "name": "Lower Abdominal Pain",
                    "parentIds": [
                        15
                    ],
                    "origId": 253273,
                    "otherNames": "Lower abdominal pain, R10.3",
                    "type": "MetaNode",
                    "id": 1251
                }
            ],
            "pageIndex": 0,
            "pageSize": 25,
            "pageCount": 1
        }

        params = {"name": "lower ABDOMINAL Pain"}
        url = self.get_service_url("/4/meta/search/")
        response_code, response_headers, response_body = self.rest_get(url, params)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def test_meta_search_by_other_names(self):
        expected = {
            "items": [
                {
                    "name": "Lower Abdominal Pain",
                    "parentIds": [
                        15
                    ],
                    "origId": 253273,
                    "otherNames": "Lower abdominal pain, R10.3",
                    "type": "MetaNode",
                    "id": 1251
                },
                {
                    "name": "Lower Belly Pain",
                    "parentIds": [
                        15
                    ],
                    "origId": 253264,
                    "otherNames": "Lower belly pain, R10.3",
                    "type": "MetaNode",
                    "id": 1253
                },
                {
                    "name": "Lower Tummy Ache",
                    "parentIds": [
                        15
                    ],
                    "origId": 253270,
                    "otherNames": "Lower tummy ache, R10.3",
                    "type": "MetaNode",
                    "id": 1255
                },
                {
                    "name": "Lower Tummy Pain",
                    "parentIds": [
                        15
                    ],
                    "origId": 253267,
                    "otherNames": "Lower tummy pain, R10.3",
                    "type": "MetaNode",
                    "id": 1257
                }
            
            ],
            "pageIndex": 0,
            "pageSize": 25,
            "pageCount": 1
        }

        params = {"name": "R10.3"}
        url = self.get_service_url("/4/meta/search/")
        response_code, response_headers, response_body = self.rest_get(url, params)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertDictEqual(expected, result)

    def test_meta_search_large_results(self):
        params = {"name": "a"}
        url = self.get_service_url("/4/meta/search/")
        response_code, response_headers, response_body = self.rest_get(url, params)
        result = JSONParser.to_collection(response_body)

        self.assertEquals(response_code, 200)
        self.assertGreaterEqual(result["pageCount"], 2)
