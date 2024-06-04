from django import template
from django.db.models import Count
from ..models import Article, Comment

register = template.Library()

@register.inclusion_tag("article/components/articles_tag_component.html")
def show_latest_articles(count=10):
    latest_articles = Article.published.all()[:count]
    return {"articles": latest_articles}


@register.inclusion_tag("article/components/articles_tag_component.html")
def show_most_controversial_articles(count=5):

    most_controversial = Article.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    
    return {
        "articles": most_controversial,
        
    }

@register.inclusion_tag("article/components/latest_comments.html")
def show_latest_comments(count=10):

    latest_comments = Comment.objects.all()[:count]
    
    return {
        "latest_comments": latest_comments,
        
    }
