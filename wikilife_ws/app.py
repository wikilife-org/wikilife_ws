# coding=utf-8

from wikilife_biz.utils.biz_service_builder import BizServiceBuilder
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_data.utils.db_conn import DBConn
from wikilife_ws.rest.dummy import V4DummyHandler, V4PostDummyHandler
from wikilife_ws.rest.global_stats import AggregationGlobalStatsHandler, \
    ExerciseGlobalStatsHandler, SocialGlobalStatsHandler, \
    EducationGlobalStatsHandler, WorkGlobalStatsHandler, \
    HealthGlobalComplaintsRankingHandler
from wikilife_ws.rest.internal_stats import InternalStatsHandler
from wikilife_ws.rest.logs import LogsHandler, LatestFinalLogsHandler
from wikilife_ws.rest.meta import MetaNodeByIdHandler, \
    MetaNodeWithMetricsHandler, MetaNodeByOrigIdHandler, MetaNodeParentsHandler, \
    MetaNodeAncestorsHandler, MetaNodeChildrenHandler, MetaSearchHandler
from wikilife_ws.rest.user_stats import HealthUserComplaintsRankingHandler
from wikilife_ws.rest.users import UserNameCheckAvailabilityHandler, \
    UserLoginHandler, EditUserNameHandler, EditPinHandler, UserAccountHandler, \
    UserProfileHandler
from wikilife_ws.rest.was2 import GlobalWasHandler, UserWasHandler
import tornado.web


def _create_service_builder(settings):
    logger = settings["LOGGER"]
    db_user = None
    db_pass = None
    db_conn = DBConn(settings["DB_SETTINGS"], db_user, db_pass)
    dao_builder = DAOBuilder(logger, db_conn)
    return BizServiceBuilder(settings, logger, dao_builder)

def _build_services(settings):
    srv_builder = _create_service_builder(settings)

    services = {}
    services["meta"] = srv_builder.build_meta_service()
    services["log"] = srv_builder.build_log_service()
    services["gs"] = srv_builder.build_gs_service()
    services["user"] = srv_builder.build_user_service()
    services["oauth"] = srv_builder.build_oauth_service()
    services["account"] = srv_builder.build_account_service()
    services["profile"] = srv_builder.build_profile_service()
    services["stat"] = srv_builder.build_stat_service()
    
    return services

def setup_app(settings):
    # intialize tornado instance

    services = _build_services(settings)

    routes = []

    routes.append(('/4/dummy', V4DummyHandler, {'services': services}))
    routes.append(('/4/postdummy', V4PostDummyHandler, {'services': services}))

    routes.append(('/4/meta/(?P<node_id>[-\w]+)', MetaNodeByIdHandler, {'services': services}))
    routes.append(('/4/meta/withmetrics/(?P<node_id>[-\w]+)', MetaNodeWithMetricsHandler, {'services': services}))
    routes.append(('/4/meta/origid/(?P<node_orig_id>[-\w]+)', MetaNodeByOrigIdHandler, {'services': services}))
    routes.append(('/4/meta/parents/(?P<node_id>[-\w]+)', MetaNodeParentsHandler, {'services': services}))
    routes.append(('/4/meta/ancestors/(?P<node_id>[-\w]+)', MetaNodeAncestorsHandler, {'services': services}))
    routes.append(('/4/meta/children/(?P<node_id>[-\w]+)', MetaNodeChildrenHandler, {'services': services}))
    routes.append(('/4/meta/search/', MetaSearchHandler, {'services': services}))
    
    routes.append(('/4/logs/', LogsHandler, {'services': services}))
    #routes.append(('/4/logs/latest', LatestFinalLogsHandler, {'services': services}))

    routes.append(('/4/user/check/', UserNameCheckAvailabilityHandler, {'services': services}))
    routes.append(('/4/user/login/', UserLoginHandler, {'services': services}))
    routes.append(('/4/user/name/', EditUserNameHandler, {'services': services}))
    routes.append(('/4/user/pin/', EditPinHandler, {'services': services}))
    routes.append(('/4/user/account/', UserAccountHandler, {'services': services}))
    routes.append(('/4/user/profile', UserProfileHandler, {'services': services}))

    #routes.append(('/4/was', GlobalWasHandler, {'services': services}))
    #routes.append(('/4/was/user', UserWasHandler, {'services': services}))

    routes.append(('/4/stats/global/aggregation/', AggregationGlobalStatsHandler, {'services': services}))
    routes.append(('/4/stats/global/exercise/times_per_week/avg', ExerciseGlobalStatsHandler, {'services': services}))
    routes.append(('/4/stats/global/social/', SocialGlobalStatsHandler, {'services': services}))
    routes.append(('/4/stats/global/education/level/', EducationGlobalStatsHandler, {'services': services}))
    routes.append(('/4/stats/global/work/experience/', WorkGlobalStatsHandler, {'services': services}))
    routes.append(('/4/stats/global/health/complaints/mostpopular/500', HealthGlobalComplaintsRankingHandler, {'services': services}))

    routes.append(('/4/stats/user/health/complaints/mostpopular/500', HealthUserComplaintsRankingHandler, {'services': services}))
    
    routes.append(('/4/stats/internal', InternalStatsHandler, {'services': services}))


    settings["TORNADO"]['logger'] = settings["LOGGER"]
    app = tornado.web.Application(routes, **settings["TORNADO"])

    return app
