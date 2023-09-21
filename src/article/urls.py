from django.urls import include, path

from .views import (ajax_vote_actions, article_detail, list_articles,
                    user_followings_articles)

app_name = "article"

urlpatterns = [
    path('', list_articles, name="articles_list"),
    # path('articles/', list_articles, name="articles_list"),
    path('tag/<str:tag_name>/', list_articles, name="articles_list_by_tag"),
    path('following/articles/', user_followings_articles, name="followings_articles"),
    path('detail/<str:title>/', article_detail, name="article_detail"),
    path('ajax/vote_actions/', ajax_vote_actions, name="ajax_vote_actions"),
]
