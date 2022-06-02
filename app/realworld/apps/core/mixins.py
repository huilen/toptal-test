from django.contrib.auth.mixins import LoginRequiredMixin


class AuthorRequiredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
