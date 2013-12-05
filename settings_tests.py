# coding=utf-8

#===================================
#   TESTS SETTINGS
#===================================

from settings import *

DB_SETTINGS = {
    "db_users"        : {"host": "localhost", "port": 27017, "name": "wikilife_users"},
    "db_logs"         : {"host": "localhost", "port": 27017, "name": "wikilife_logs"},
    "db_processors"   : {"host": "localhost", "port": 27017, "name": "wikilife_processors"},
    "db_crawler"      : {"host": "localhost", "port": 27017, "name": "wikilife_crawler"},
    "db_apps"         : {"host": "localhost", "port": 27017, "name": "wikilife_apps"},
    "db_admin"        : {"host": "localhost", "port": 27017, "name": "wikilife_admin"}
}
DB_SETTINGS["db_meta_live"]["uri"] = "http://localhost:7474/db/data/"

QUEUE_LOGS = {"host": "localhost", "port": 5672, "name": "log_queue"}
QUEUE_OPERS = {"host": "localhost", "port": 5672, "name": "oper_queue"}
WS_HOST = "http://localhost:7080"
