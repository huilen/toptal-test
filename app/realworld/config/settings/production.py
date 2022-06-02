# flake8: noqa

import dj_database_url

from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


sentry_sdk.init(
    dsn="https://c00cc5768fbc446bbccc03dcb3db3779@o1267411.ingest.sentry.io/6453689",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE.insert(5, "django.middleware.gzip.GZipMiddleware")


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# ==============================================================================
# WHITENOISE SETTINGS
# ==============================================================================

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
