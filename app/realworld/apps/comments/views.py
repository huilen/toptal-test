from django.views.generic import DeleteView

from realworld.apps.core.mixins import AuthorRequiredMixin

from .models import Comment


class CommentDeleteView(AuthorRequiredMixin, DeleteView):
    model = Comment
    success_url = "/"
