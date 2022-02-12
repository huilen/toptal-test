# flake8: noqa

from .base import *

import dj_database_url


DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
