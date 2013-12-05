# coding=utf-8

#===================================
#   QA ENVIRONMENT SETTINGS
#===================================
#Tornado run on DEV machine

from settings import *


# The following will be used for any DB that does not EXPLICITLY override these values.
DB_SETTINGS_DEFAULT = {
    "host": "dev2",
    "port": 27027,
}

DB_SETTINGS["db_meta_live"]["uri"] = "http://dev2:7474/db/data/"

DB_SETTINGS["db_location"]["port"] = 5432
DB_SETTINGS["db_location"]["user"] = "postgres"
DB_SETTINGS["db_location"]["pass"] = "123456"

QUEUE_LOGS = {"host": "localhost", "port": 5672, "name": "qa_log_queue"}
QUEUE_OPERS = {"host": "localhost", "port": 5672, "name": "qa_oper_queue"}

DASNIA_SETTINGS["singly"] = {}
DASNIA_SETTINGS["singly"]["client_id"] = " cf588c00ec214e2503b958569161ac39"
DASNIA_SETTINGS["singly"]["client_secret"] = "a1d1a3e3e3683733a30f150b7d1361e8"
DASNIA_SETTINGS["singly"]["api_root"] = "https://api.singly.com/"
DASNIA_SETTINGS["singly"]["api_access_token_url"] = DASNIA_SETTINGS["singly"]["api_root"] + "oauth/access_token"
DASNIA_SETTINGS["singly"]["api_push_url"] = DASNIA_SETTINGS["singly"]["api_root"] + "push"
DASNIA_SETTINGS["singly"]["push_listener_base_url"] = "http://localhost:7080/2/dasnia/singly/push/"
DASNIA_SETTINGS["singly"]["api_services_url"] = DASNIA_SETTINGS["singly"]["api_root"] + "services"
DASNIA_SETTINGS["singly"]["api_services_urls"] = {}
#DASNIA_SETTINGS["singly"]["api_services_urls"]["tweeter"] = DASNIA_SETTINGS["singly"]["api_services_url"] + "/twitter/tweets" 
DASNIA_SETTINGS["singly"]["api_services_urls"]["fitbit"] = DASNIA_SETTINGS["singly"]["api_services_url"] + "/fitbit/activities"
DASNIA_SETTINGS["singly"]["api_services_urls"]["runkeeper"] = DASNIA_SETTINGS["singly"]["api_services_url"] + "/runkeeper/fitness_activities"
DASNIA_SETTINGS["singly"]["api_services_urls"]["withings"] = DASNIA_SETTINGS["singly"]["api_services_url"] + "/withings/measures"
DASNIA_SETTINGS["singly"]["api_services_urls"]["zeo"] = DASNIA_SETTINGS["singly"]["api_services_url"] + "/zeo/sleep_records"
