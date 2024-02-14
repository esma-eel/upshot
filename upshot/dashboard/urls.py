from django.urls import path

from .views import (
    ajax_article_actions,
    ajax_comment_actions,
    ajax_follow_unfollow,
    ajax_mentor_request_actions,
    create_article,
    dashboard,
    edit_article,
    mentor_setting,
    profile_edit,
    user_articles_management,
    user_followers_management,
    user_followings_management,
    user_get_comments_management,
    user_inbox_request_management,
    user_profile,
    user_registration,
    user_sent_comments_management,
    user_sent_request_management,
)

urlpatterns = [
    path("register/", user_registration, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/profile_edit/", profile_edit, name="profile_edit"),
    path("dashboard/mentor_setting/", mentor_setting, name="mentor_setting"),
    path(
        "dashboard/followers/",
        user_followers_management,
        name="followers_management",
    ),
    path(
        "dashboard/followings/",
        user_followings_management,
        name="followings_management",
    ),
    path(
        "dashboard/articles/",
        user_articles_management,
        name="articles_management",
    ),
    path("dashboard/articles/create/", create_article, name="create_article"),
    path(
        "dashboard/articles/edit/<int:id>/", edit_article, name="edit_article"
    ),
    path(
        "dashboard/sent_comments/",
        user_sent_comments_management,
        name="sent_comments_management",
    ),
    path(
        "dashboard/get_comments/",
        user_get_comments_management,
        name="get_comments_management",
    ),
    path(
        "dashboard/sent_request/",
        user_sent_request_management,
        name="sent_request_management",
    ),
    path(
        "dashboard/inbox_request/",
        user_inbox_request_management,
        name="inbox_request_management",
    ),
    path("<username>/", user_profile, name="user_profile"),
    # ajax
    path(
        "ajax/follow_unfollow/",
        ajax_follow_unfollow,
        name="ajax_follow_unfollow",
    ),
    path(
        "ajax/article_actions/",
        ajax_article_actions,
        name="ajax_article_actions",
    ),
    path(
        "ajax/comment_actions/",
        ajax_comment_actions,
        name="ajax_comment_actions",
    ),
    path(
        "ajax/mentor_request_actions/",
        ajax_mentor_request_actions,
        name="ajax_mentor_request_actions",
    ),
]
