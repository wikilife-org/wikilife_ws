import tornado.web

from wikilife_ws.rest import dummy, meta, logs, users, was2, global_stats,\
    user_stats, internal_stats


def setup_app(settings):
    # intialize our tornado instance
    routes = []
    #routes.extend(_test.routes)
    routes.extend(dummy.routes)
    routes.extend(logs.routes)
    routes.extend(users.routes)
    #routes.extend(user_settings.routes)
    #routes.extend(profile.routes)
    #routes.extend(security_questions.routes)
    routes.extend(was2.routes)
    routes.extend(global_stats.routes)
    routes.extend(user_stats.routes)
    routes.extend(internal_stats.routes)
    #routes.extend(timeline.routes)
    #routes.extend(questions.routes)
    #routes.extend(notifications.routes)
    routes.extend(meta.routes)
    #routes.extend(dasnia.routes)
    #routes.extend(oauth.routes)
    #routes.extend(developers.routes)
    #routes.extend(location.routes)

    app = tornado.web.Application(routes, **settings)
    return app
