from django.contrib.postgres.search import SearchVector
from django_filters import rest_framework as filters
from taggit.models import Tag
from upshot.article.models import Article, Comment


class ArticleFilterSet(filters.FilterSet):
    search__title_body = filters.CharFilter(method="search_articles")
    search__tags = filters.CharFilter(method="search_tags")

    class Meta:
        model = Article
        exclude = ["picture", "tags"]

    def search_articles(self, queryset, name, value):
        article_qs = queryset.annotate(
            search=SearchVector("title", "body"),
        ).filter(search=value, status="published")

        return article_qs

    def search_tags(self, queryset, name, value):
        tag_qs = Tag.objects.filter(name=value)
        if tag_qs.exists():
            article_qs = queryset.filter(tags__in=tag_qs, status="published")
            return article_qs

        return queryset


class CommentFilterSet(filters.FilterSet):
    class Meta:
        model = Comment
        exclude = []
