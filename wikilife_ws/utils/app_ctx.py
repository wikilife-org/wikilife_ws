# coding=utf-8


class AppCTX(object):
    """
    TMP Singleton util Tornado's app ctx can be used
    """

    _instance = None

    @staticmethod
    def get_instance():
        if AppCTX._instance == None:
            AppCTX._instance = AppCTX()

        return AppCTX._instance

    settings = None
    logger = None
    service_builder = None
