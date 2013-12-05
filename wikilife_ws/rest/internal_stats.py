# coding=utf-8

from wikilife_utils.date_utils import DateUtils
from wikilife_utils.mail.simple_mail_sender import SinpleMailSender
from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.route import Route

class BaseInternalStatHandler(BaseHandler):

    def initialize(self):
        super(BaseInternalStatHandler, self).initialize()
        self._stat_srv = self._service_builder.build_stat_service()


@Route('/4/stats/internal')
class InternalStatsHandler(BaseInternalStatHandler):
    """
    """

    def get(self):
        try:

            report = {}
            report["datetime_utc"] = DateUtils.get_datetime_utc()
            report["groups"] = self._get_report_groups()

            try:
                frm = "noreply@wikilife.org"
                to = [self.get_argument("to", "dev@wikilife.org")]
                subject = "Wikilife Daily Stats: %s-%s-%s" %(report["datetime_utc"].year, report["datetime_utc"].month, report["datetime_utc"].day)
                text_body = self._report_to_text_body(report)
                html_body = self._report_to_html_body(report)
                SinpleMailSender("localhost").send_html_mail(frm, to, subject, text_body, html_body)

            except Exception, e:
                self._logger.exception(e)

            self.success(report)

        except Exception, e:
            self._logger.exception(e)
            self.error(str(e))

    def _get_report_groups(self):
        groups = []
        
        internal_stats = self._stat_srv.get_stat_by_id(1000)
        user_stats = internal_stats["data"]["users"]
        log_stats = internal_stats["data"]["logs"]
        
        users = {"title": "Users", "items": []}
        users["items"].append({"title": "All", "total": user_stats["all"]["total"], "yesterday": user_stats["all"]["yesterday"]})
        users["items"].append({"title": "WL Apps", "total": user_stats["wlApps"]["total"], "yesterday": user_stats["wlApps"]["yesterday"]})
        users["items"].append({"title": "External", "total": user_stats["external"]["total"], "yesterday": user_stats["external"]["yesterday"]})
        users["items"].append({"title": "Active", "total": user_stats["active"]["lastmonth"], "yesterday": user_stats["active"]["yesterday"]})
        groups.append(users)

        logs = {"title": "Logs", "items": []}
        logs["items"].append({"title": "All", "total": 0, "yesterday": 0})

        for item in log_stats:
            logs["items"][0]["total"] += item["total"]
            logs["items"][0]["yesterday"] += item["yesterday"]
            logs["items"].append({"title": item["name"], "total": item["total"], "yesterday": item["yesterday"]})

        groups.append(logs)

        return groups

    def _report_to_text_body(self, report):
        body = "      Total, Yesterday\n\n"

        for group in report["groups"]:
            body += "%s: \n" %group["title"]

            for item in group["items"]:
                body += "  %s: %s, %s \n" %(item["title"], item["total"], item["yesterday"])

        return body

    def _report_to_html_body(self, report):
        body = "<table><tr><td></td><td>Total</td><td>Yesterday</td></tr>"
        
        for group in report["groups"]:
            body += '<tr><td colspan="3">%s</td></tr>' %group["title"]

            for item in group["items"]:
                body += "<tr><td>%s: &nbsp;</td><td>%s &nbsp; &nbsp;</td><td>%s</td></tr>" %(item["title"], item["total"], item["yesterday"])

            body += '<tr><td colspan="3" height="10">&nbsp;</td></tr>'
            
        body += "</table>"
        return body


routes = Route.get_routes()
