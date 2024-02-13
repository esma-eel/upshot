from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# custom manager to get all of the published posts at once
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PublishedManager, self)
            .get_queryset()
            .filter(status="published")
        )


class Article(models.Model):
    STATUS_CHOICES = (("draft", "پیشنویس"), ("published", "منتشر شده"))

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles"
    )
    # upload picture to paht based on upload date
    picture = models.ImageField(upload_to="articles/%Y/%m/%d", blank=True)
    body = RichTextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    users_positive_vote = models.ManyToManyField(
        User, related_name="articles_voted_positive", blank=True
    )
    users_negative_vote = models.ManyToManyField(
        User, related_name="articles_voted_negative", blank=True
    )
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse("article:article_detail", args=[self.slug])
        return url


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "نظر توسط {} روی مقاله {}".format(
            self.user.username, self.article
        )

    def get_absolute_url(self):
        return self.article.get_absolute_url()
