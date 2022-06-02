from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from taggit.models import Tag

from realworld.apps.comments.forms import Comment, CommentForm
from realworld.apps.core.mixins import AuthorRequiredMixin, LoginRequiredMixin

from .forms import Article, ArticleForm


class ArticleListView(ListView):
    context_object_name = "articles"
    template_name = "realworld/articles/article_list.html"

    def get_queryset(self):
        queryset = (
            Article.objects.select_related("author")
            .with_favorites(self.request.user)
            .prefetch_related("tags")
            .order_by("-created")
        )

        if tag := self.request.GET.get("tag"):
            return queryset.filter(tags__name__in=[tag])

        if self.request.user.is_authenticated and "own" in self.request.GET:
            return queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class ArticleDetailView(DetailView):
    context_object_name = "article"
    template_name = "realworld/articles/article_detail.html"

    def get_queryset(self):
        queryset = Article.objects.select_related("author").with_favorites(
            self.request.user
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_following = self.object.author.following.filter(
            pk=self.request.user.id
        ).exists()
        comments = (
            Comment.objects.filter(article=self.kwargs["pk"])
            .select_related("author")
            .order_by("-created")
        )

        context["is_following"] = is_following
        context["comments"] = comments
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment = Comment(
            content=request.POST.get("content"),
            author=self.request.user,
            article=self.get_object(),
        )
        comment.save()
        return self.get(self, request, *args, **kwargs)


class ArticleCreateView(AuthorRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "realworld/articles/article_form.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()

        # save tags
        form.save_m2m()

        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "realworld/articles/article_form.html"


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    model = Article
    success_url = "/"


class ArticleFavoriteView(LoginRequiredMixin, UpdateView):
    fields = ["favorites"]
    http_method_names = ["post"]

    def get_queryset(self):
        return Article.objects.select_related("author").exclude(
            author=self.request.user
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.favorites.filter(id=request.user.id).exists():
            self.object.favorites.remove(request.user)
        else:
            self.object.favorites.add(request.user)

        return redirect(self.object.get_absolute_url())
