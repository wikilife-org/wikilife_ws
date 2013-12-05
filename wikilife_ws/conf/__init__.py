"""
Settings and configuration for Wikilife
"""

import os
import sys

ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


class Settings(object):
    def __init__(self):
        # store the settings module in case someone later cares

        self.SETTINGS_MODULE = "settings_%s" % os.environ[ENVIRONMENT_VARIABLE]

        try:
            global_settings = __import__(self.SETTINGS_MODULE)
            sys.modules[self.SETTINGS_MODULE]
            import settings as main_settings
            total_settings = dir(global_settings)
            total_settings.extend(dir(main_settings))
            for setting in total_settings:
                if setting == setting.upper():
                    try:
                        setattr(self, setting, getattr(main_settings, setting))
                    except:
                        setattr(self, setting, getattr(global_settings, setting))

        except ImportError, e:
            raise ImportError("Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (self.SETTINGS_MODULE, e))

settings = Settings()
