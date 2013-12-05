# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.route import Route


class BaseMetaHandler(BaseHandler):

    _meta_srv = None

    def initialize(self):
        super(BaseMetaHandler, self).initialize()
        self._meta_srv = self._service_builder.build_meta_service()


@Route("/4/meta/(?P<node_id>[-\w]+)")
class MetaNodeByIdHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        node = self._meta_srv.get_node_by_id(int(node_id))
        self.success(node)


@Route("/4/meta/withmetrics/(?P<node_id>[-\w]+)")
class MetaNodeWithMetricsHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        node = self._meta_srv.get_node_with_metrics(int(node_id))
        self.success(node)


@Route("/4/meta/origid/(?P<node_orig_id>[-\w]+)")
class MetaNodeByOrigIdHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_orig_id):
        node = self._meta_srv.get_node_by_orig_id(int(node_orig_id))
        self.success(node)


@Route("/4/meta/parents/(?P<node_id>[-\w]+)")
class MetaNodeParentsHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        nodes = self._meta_srv.get_node_parents(int(node_id))
        self.success(nodes)

@Route("/4/meta/ancestors/(?P<node_id>[-\w]+)")
class MetaNodeAncestorsHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        nodes = self._meta_srv.get_node_ancestors(int(node_id))
        self.success(nodes)


@Route("/4/meta/children/(?P<node_id>[-\w]+)")
class MetaNodeChildrenHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        params = self.get_params()
        page_index = params.get("page", 0)
        nodes_page = self._meta_srv.get_node_children(int(node_id), int(page_index))
        self.success(nodes_page)


@Route("/4/meta/search/")
class MetaSearchHandler(BaseMetaHandler):
    """
    """

    @catch_exceptions
    def get(self):
        params = self.get_str_params()
        name = params["name"]
        page_index = int(params.get("page", 0))
        node_list = self._meta_srv.find_nodes(name, page_index)
        self.success(node_list)


routes = Route.get_routes()
