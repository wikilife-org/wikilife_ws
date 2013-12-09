# coding=utf-8

from wikilife_ws.rest.base_handler import BaseHandler
from wikilife_ws.utils.catch_exceptions import catch_exceptions


class MetaNodeByIdHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        meta_srv = self._services["meta"]
        node = meta_srv.get_node_by_id(int(node_id))
        self.success(node)


class MetaNodeWithMetricsHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        meta_srv = self._services["meta"]
        node = meta_srv.get_node_with_metrics(int(node_id))
        self.success(node)


class MetaNodeByOrigIdHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_orig_id):
        meta_srv = self._services["meta"]
        node = meta_srv.get_node_by_orig_id(int(node_orig_id))
        self.success(node)


class MetaNodeParentsHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        meta_srv = self._services["meta"]
        nodes = meta_srv.get_node_parents(int(node_id))
        self.success(nodes)


class MetaNodeAncestorsHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        meta_srv = self._services["meta"]
        nodes = meta_srv.get_node_ancestors(int(node_id))
        self.success(nodes)


class MetaNodeChildrenHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self, node_id):
        meta_srv = self._services["meta"]
        params = self.get_params()
        page_index = params.get("page", 0)
        nodes_page = meta_srv.get_node_children(int(node_id), int(page_index))
        self.success(nodes_page)


class MetaSearchHandler(BaseHandler):
    """
    """

    @catch_exceptions
    def get(self):
        meta_srv = self._services["meta"]
        params = self.get_str_params()
        name = params["name"]
        page_index = int(params.get("page", 0))
        node_list = meta_srv.find_nodes(name, page_index)
        self.success(node_list)
