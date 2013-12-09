# coding=utf-8

from getopt import getopt, GetoptError
import json
import os
import sys
import tornado.httpserver
import tornado.ioloop

DEFAULT_ENV = 'local'
DEFAULT_PORT = '7080'
DEFAULT_LIBS_PATH = '..'


def start_instance(settings):
    from wikilife_ws.app import setup_app
    http_server = tornado.httpserver.HTTPServer(
        setup_app(settings)
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
    usage = \
"""Usage:

  {filename} [runserver] [--env ENV] [--port PORT] [--libs LIBPATH]
""" \
.format(filename=sys.argv[0])
    print(usage)


if __name__ == "__main__":

    env = DEFAULT_ENV
    port = DEFAULT_PORT
    libs_path = DEFAULT_LIBS_PATH
    cmd = sys.argv[1]

    try:
        opts, args = getopt(sys.argv[2:], '', ['port=', 'env=', 'libs='])
    except GetoptError:
        print("Invalid arguments.")
        display_help()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '--port':
            port = arg
        elif opt == '--env':
            env = arg
        elif opt == '--libs':
            libs_path = arg
        else:
            print("Superfluous argument: {}".format(opt))

    if not cmd:
        print("No command specified.")
        display_help()
        sys.exit(0)

    sys.path.append(os.path.abspath(os.path.join(sys.argv[0], "../.."))) #export PYTHONPATH=$PYTHONPATH:$PWD;
    sys.path.append(os.path.abspath(os.path.join(libs_path, "wikilife_utils")))
    sys.path.append(os.path.abspath(os.path.join(libs_path, "wikilife_data")))
    sys.path.append(os.path.abspath(os.path.join(libs_path, "wikilife_biz")))
    
    from wikilife_utils.settings.settings_loader import SettingsLoader
    settings = SettingsLoader().load_settings(env)
    settings["TORNADO"]["port"] = port

    if cmd == "runserver":
        start_instance(settings)

    elif cmd == "help":
        display_help()

    else:
        print "Unknown command '%s'" % cmd
        display_help()
