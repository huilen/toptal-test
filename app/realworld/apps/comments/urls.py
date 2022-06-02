from django.urls import path

from .views import CommentDeleteView

app_name = "comments"

urlpatterns = [path("delete/<int:pk>/", CommentDeleteView.as_view(), name="delete")]
