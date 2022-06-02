from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("realworld.apps.articles.urls")),
    path("", include("realworld.apps.accounts.urls")),
    path("comments/", include("realworld.apps.comments.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
