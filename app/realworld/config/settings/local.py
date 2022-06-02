# flake8: noqa

from .base import *

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

TEMPLATES[0]["OPTIONS"]["debug"] = True


# Debug Toolbar
# =============

INTERNAL_IPS = ["127.0.0.1", "::1"]
