from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleFavoriteView,
    ArticleListView,
    ArticleUpdateView,
)

app_name = "articles"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("new/", ArticleCreateView.as_view(), name="create"),
    path(
        "article/<int:pk>/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="detail",
    ),
    path(
        "article/edit/<int:pk>/",
        ArticleUpdateView.as_view(),
        name="edit",
    ),
    path(
        "article/delete/<int:pk>/",
        ArticleDeleteView.as_view(),
        name="delete",
    ),
    path(
        "article/favorite/<int:pk>/",
        ArticleFavoriteView.as_view(),
        name="favorite",
    ),
]
