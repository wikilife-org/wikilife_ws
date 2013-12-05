# coding=utf-8

from wikilife_ws.tests.base_test import BaseTest


class FinalLogsLatestsTests(BaseTest):

    def test_get_latest_final_logs(self):
        '''
        @Route("/4/logs/latest")
        class LatestFinalLogsHandler(BaseLogsHandler):
            """
            """
        
            @catch_exceptions
            def get(self):
                """
                Returns the lastest `amount` logs.
                Does not include any user-sensitive inforomation.
        
                :param amount: Amount of logs to return. Defaults to 20.
        
                """
                amount = self.get_argument("amount", 20)
                latest_logs = self._gs_srv.get_latest_logs(amount)
                self.success(latest_logs)
        '''
