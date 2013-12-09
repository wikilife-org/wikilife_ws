# coding=utf-8

from os import path
import logging

#===================================
#   LOGGING
#===================================

LOGGER = logging.getLogger('wikilife ws')
handler = logging.FileHandler(path.join(path.dirname(__file__), "logs/wikilife_ws.log"))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

#===================================
#   TORNADO
#===================================

TORNADO = dict(
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

#===================================
#   DB 
#===================================

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
