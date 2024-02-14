from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from upshot.actions.utils import create_action

from .forms import CreateCommentForm, SearchForm
from .models import Article


def home_view(request):
    # search form constructor
    form = SearchForm()
    context = {"section": "home", "form": form}
    return render(request, "article/index.html", context)


def search_objects(request):
    """
    Search between articles with title, body or related tags
    Search between users who are mentor or publisher of articles
    """
    form = SearchForm()
    query = None  # field in search form
    search = None  # field in search form
    section = "search"  # for active link purpose in template
    resutls_model = ""
    results = []
    # if user inputs search query
    # method of sending data to backend is GET
    if "query" in request.GET:
        # construct search form with request
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search = form.cleaned_data["search"]
            if search == "search_article":
                # if user wants to search article
                # we search title and body together with query input
                resutls_model = "article"
                if len(query) > 0:
                    results = Article.published.annotate(
                        search=SearchVector("title", "body"),
                    ).filter(search=query)
                else:
                    results = Article.published.all()

            if search == "search_tag":
                # first we find input tag then we get articles published with it
                resutls_model = "tag"
                if len(query) > 0:
                    tag = Tag.objects.filter(name=query)
                    if tag.exists():
                        results = Article.published.filter(tags__in=tag)

            if search == "search_author":
                # we apply search for 3 fields in user object
                resutls_model = "user"
                if len(query) > 0:
                    results = User.objects.annotate(
                        search=SearchVector(
                            "username", "first_name", "last_name"
                        ),
                    ).filter(search=query)
                else:
                    results = User.objects.all()

            if search == "search_guide":
                # if mentor settings of user is active
                # and match with query input
                section = "guide_request"
                resutls_model = "user"
                if len(query) > 0:
                    results = User.objects.annotate(
                        search=SearchVector(
                            "username", "first_name", "last_name"
                        ),
                    ).filter(search=query, mentorsetting__active=True)
                else:
                    results = User.objects.filter(mentorsetting__active=True)

    # pagination
    how_many_in_a_page = 12
    results_paginator = Paginator(results, how_many_in_a_page)
    page = request.GET.get("page")
    try:
        results = results_paginator.page(page)
    except PageNotAnInteger:
        results = results_paginator.page(1)
    except EmptyPage:
        results = results_paginator.page(results_paginator.num_pages)

    # in order to show related component based on result model and
    # selected search option
    get_copy = request.GET.copy()
    params = get_copy.pop("page", True) and get_copy.urlencode()

    context = {
        "resutls_model": resutls_model,
        "results": results,
        "query": query,
        "form": form,
        "page": page,
        "search": search,
        "params": params,
        "section": section,
    }

    return render(request, "article/search_objects.html", context)


def list_articles(request, tag_name=None):
    """
    Get list of articles based on published or based on tags which
    user sent
    """
    articles = Article.published.all()
    form = SearchForm()
    tag = None

    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        articles = articles.filter(tags__in=[tag])

    # pagination
    how_many_in_a_page = 12
    articles_paginator = Paginator(articles, how_many_in_a_page)
    page = request.GET.get("page")
    try:
        articles = articles_paginator.page(page)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    except EmptyPage:
        articles = articles_paginator.page(articles_paginator.num_pages)

    context = {
        "articles": articles,
        "page": page,
        "tag": tag,
        "section": "articles",
        "form": form,
    }

    return render(request, "article/list_articles.html", context)


@login_required
def user_followings_articles(request):
    """
    Get list of articles from people the user follow
    """
    user = get_object_or_404(User, username=request.user.username)
    user_fls = user.following.all()

    if not user_fls.exists():
        return redirect("dashboard")

    articles = Article.published.filter(author__in=user_fls)

    # pagination
    how_many_in_a_page = 12
    articles_paginator = Paginator(articles, how_many_in_a_page)
    page = request.GET.get("page")
    try:
        articles = articles_paginator.page(page)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    except EmptyPage:
        articles = articles_paginator.page(articles_paginator.num_pages)

    context = {
        "articles": articles,
        "page": page,
    }

    return render(request, "article/followings_articles.html", context)


def article_detail(request, title):
    """
    Show detailts of article based on slug
    """
    # only author can see the unpublished article
    article = get_object_or_404(Article, slug=title)
    if request.user != article.author:
        article = get_object_or_404(Article, slug=title, status="published")

    # comments
    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        # comment posted
        comment_form = CreateCommentForm(data=request.POST)
        if comment_form.is_valid():
            # dont save comment yet
            new_comment = comment_form.save(commit=False)
            new_comment.article = article  # assign article
            new_comment.user = request.user
            new_comment.save()  # save comment

            action_verb_string = (
                'کاربر "{}" روی مقاله "{}" نظر ارسال کرد'.format(
                    request.user.username, new_comment.article.title
                )
            )
            create_action(request.user, action_verb_string, new_comment)

            messages.success(
                request,
                "نظر شما با موفقیت ارسال شد",
                extra_tags="alert alert-success",
            )
            return redirect(article.get_absolute_url())

    else:
        comment_form = CreateCommentForm()

    context = {
        "article": article,
        "comments": comments,
        "comment_form": comment_form,
    }

    return render(request, "article/article_detail.html", context)


@require_POST
@login_required
def ajax_vote_actions(request):
    """
    Vote for article
    """
    data = {"status": "ko"}

    if request.is_ajax():
        id = request.POST.get("id")
        action = request.POST.get("action")

        data.update(message="قبل if action and article_id")
        if action and id:
            try:
                data.update(message="توی try")
                #
                article_to_modify = Article.objects.get(id=id)
                print(article_to_modify)
                data.update(message="مقاله رو گرفتم")
                if action == "positive_vote":
                    # check if user already give negative vote
                    # remove it to create new positive vote
                    already_negative_voted = (
                        request.user.articles_voted_negative.filter(
                            id=article_to_modify.id
                        )
                    )
                    data.update(message="بعد از already negative voted")
                    if already_negative_voted.exists():
                        article_to_modify.users_negative_vote.remove(
                            request.user
                        )

                    article_to_modify.users_positive_vote.add(request.user)

                    action_verb_string = (
                        'کاربر "{}" به مقاله "{}" رای داد'.format(
                            request.user.username, article_to_modify.title[:30]
                        )
                    )
                    create_action(
                        request.user, action_verb_string, article_to_modify
                    )

                    data.update(status="ok")
                    data.update(message="رای مثبت شما ثبت شد")
                    return JsonResponse(data)

                if action == "negative_vote":
                    # check if user already give positive vote
                    # remove it to create new negative vote
                    already_positive_voted = (
                        request.user.articles_voted_positive.filter(
                            id=article_to_modify.id
                        )
                    )

                    data.update(message="بعد از already positive voted")
                    if already_positive_voted.exists():
                        article_to_modify.users_positive_vote.remove(
                            request.user
                        )

                    article_to_modify.users_negative_vote.add(request.user)

                    action_verb_string = (
                        'کاربر "{}" به مقاله "{}" رای داد'.format(
                            request.user.username, article_to_modify.title[:30]
                        )
                    )
                    create_action(
                        request.user, action_verb_string, article_to_modify
                    )

                    data.update(status="ok")
                    data.update(message="رای منفی شما ثبت شد")
                    return JsonResponse(data)
                return JsonResponse(data)

            except Article.DoesNotExist:
                data.update(message="توی قسمت اکسپت")
                return JsonResponse(data)

    data.update(message="قبل آخرین جیسون ریسپانس")
    return JsonResponse(data)
