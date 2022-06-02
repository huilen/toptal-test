from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, ListView, UpdateView

from realworld.apps.articles.models import Article

from .forms import SettingsForm, User, UserCreationForm


class ProfileView(ListView):
    context_object_name = "articles"
    template_name = "realworld/accounts/profile.html"

    def get_queryset(self):
        profile = get_object_or_404(User, pk=self.kwargs["pk"])
        articles = (
            Article.objects.select_related("author")
            .with_favorites(self.request.user)
            .prefetch_related("tags")
            .order_by("-created")
        )

        if "favorites" in self.request.GET:
            return articles.filter(is_favorite=True)

        return articles.filter(author=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, pk=self.kwargs["pk"])
        context["profile"] = profile
        context["is_following"] = profile.following.filter(
            pk=self.request.user.id
        ).exists()
        return context


class SettingView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SettingsForm
    template_name = "realworld/accounts/settings.html"

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "registration/register.html"
    redirect_authenticated_user = False

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a register page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    def get_success_url(self):
        return '/'


class ProfileFollowView(LoginRequiredMixin, UpdateView):
    fields = ["following"]
    http_method_names = ["post"]

    def get_queryset(self, **kwargs):
        return User.objects.filter(pk=self.kwargs["pk"]).exclude(
            pk=self.request.user.id
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.following.filter(id=request.user.id).exists():
            self.object.following.remove(request.user)
        else:
            self.object.following.add(request.user)

        return redirect(self.object.get_absolute_url())
