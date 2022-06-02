from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

import markdown
from taggit.managers import TaggableManager


class ArticleQuerySet(models.QuerySet):
    def with_favorites(self, user):
        return self.annotate(
            num_favorites=models.Count("favorites"),
            is_favorite=models.Exists(
                get_user_model().objects.filter(
                    pk=user.id, favorites=models.OuterRef("pk")
                ),
            )
            if user.is_authenticated
            else models.Value(False, output_field=models.BooleanField()),
        )


ArticleManager = models.Manager.from_queryset(ArticleQuerySet)


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorites"
    )

    objects = ArticleManager()

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse(
            "articles:detail",
            kwargs={
                "pk": self.id,
                "slug": self.slug,
            },
        )

    def as_markdown(self):
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])
