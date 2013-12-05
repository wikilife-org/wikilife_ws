# coding=utf-8

from wikilife_biz.utils.biz_service_builder import BizServiceBuilder
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_data.utils.db_conn import DBConn
from wikilife_utils.settings.settings_loader import SettingsLoader
from wikilife_ws.app import setup_app
from wikilife_ws.utils.app_ctx import AppCTX
import json
import sys
import tornado.httpserver
import tornado.ioloop


def start_instance(settings):

    app_ctx = AppCTX.get_instance()
    app_ctx.settings = settings
    app_ctx.logger = settings["LOGGER"]
    app_ctx.service_builder = _create_service_builder(settings)

    http_server = tornado.httpserver.HTTPServer(
        setup_app(settings["TORNADO"])
        )
    http_server.listen(settings["TORNADO"]["port"])

    display_server_info(settings)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

    print "started"


def display_server_info(settings):
    print ""
    print "===== SERVER INFO ====="
    print ""
    print "Server: Wikilife WS (Tornado)"
    print "Environment: %s" % settings["ENVIRONMENT"]
    print "Port: %s" % settings["TORNADO"]["port"]
    print "DB_SETTINGS: %s" % json.dumps(settings["DB_SETTINGS"], indent=2)
    print ""
    print "======================="
    print ""


def display_help():
    print "Use: {environment=prod, qa, dev, local} runserver {port}"


def _create_service_builder(settings):
    logger = settings["LOGGER"]
    db_user = None
    db_pass = None
    db_conn = DBConn(settings["DB_SETTINGS"], db_user, db_pass)
    dao_builder = DAOBuilder(logger, db_conn)
    return BizServiceBuilder(settings, logger, dao_builder)

if __name__ == "__main__":
    env = str(sys.argv[1])
    cmd = str(sys.argv[2])
    port = str(sys.argv[3])
    settings = SettingsLoader().load_settings(env)
    settings["TORNADO"]["port"] = port

    if cmd == "runserver":
        start_instance(settings)

    elif cmd == "help":
        display_help()

    else:
        print "Unknown command '%s'" % cmd
        display_help()
