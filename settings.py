# coding=utf-8

from os import path
import datetime
import logging
import pytz


RELEASE_DATETIME = datetime.datetime(2011, 12, 27, tzinfo=pytz.utc)

#===================================
#   LOGGING
#===================================

LOGGER = logging.getLogger('wikilife ws')
hdlr = logging.FileHandler(path.join(path.dirname(__file__), "logs/wikilife_ws.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.INFO)

#===================================
#   TORNADO
#===================================

TORNADO = dict(
    port=6488,
    db_name="",
    db_uri="",
    db_user="",
    db_pass="",
    login_url="/auth/login",
    static_path=path.join(path.dirname(__file__), "static"),
    template_path=path.join(path.dirname(__file__), "templates"),
    cookie_secret="SOMETHING HERE",
    debug=False,
    debug_pdb=False,
)

DB_SETTINGS = {
    "db_meta_live": {},
    "db_meta_edit": {},
    "db_users": {"name": "wikilife_users"},
    "db_logs": {"name": "wikilife_logs"},
    "db_processors": {"name": "wikilife_processors"},
    "db_crawler": {"name": "wikilife_crawler"},
    "db_apps": {"name": "wikilife_apps"},
    "db_admin": {"name": "wikilife_admin"},
    "db_location": {"name": "geonames"}
}

DASNIA_SETTINGS = {}
