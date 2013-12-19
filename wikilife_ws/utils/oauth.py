# coding=utf-8

import functools


def authenticated(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user_id = self.get_user_for_token(self.get_argument('oauth_token'))
        # TODO XXX: if user_id == None: throw 401
        return method(self, user_id=user_id, *args, **kwargs)
    return wrapper


def userless(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO: make sure that client_id exists
        return method(self, *args, **kwargs)
    return wrapper


def authenticated_developer(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # TODO: manage token expiration
        developer_id = self.get_developer_for_token(self.get_argument('session_token'))
        return method(self, developer_id=developer_id, *args, **kwargs)
    return wrapper
