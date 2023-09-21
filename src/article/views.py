from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from taggit.models import Tag

from actions.utils import create_action
from mentor.models import MentorRequest, MentorSetting

from .forms import CreateCommentForm, SearchForm
from .models import Article, Comment


def home_view(request):
    form = SearchForm()
    context = {"section": "home", 'form': form}
    return render(request, "article/index.html", context)


def search_objects(request):
    form = SearchForm()
    query = None
    search = None
    section = "search"
    resutls_model = ''
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
    #         CHOICES_SEARCH = (
    #     ('search_article', 'مقاله'),
    #     ('search_author', 'نویسنده'),
    #     ('search_tag', 'برچسب'),
    #     ('search_guide', 'راهنما')
    # )
            query = form.cleaned_data['query']
            search = form.cleaned_data['search']
            if search == 'search_article':
                resutls_model = 'article'
                if len(query) > 0:
                    results = Article.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
                else:
                    results = Article.published.all()

            if search == 'search_tag':
                resutls_model = 'tag'
                if len(query) > 0:
                    tag = Tag.objects.filter(name=query)
                    if tag.exists():
                        results = Article.published.filter(tags__in=tag)
                    
            if search == 'search_author':
                resutls_model = 'user'
                if len(query) > 0:
                    results = User.objects.annotate(search=SearchVector('username', 'first_name', 'last_name'),).filter(search=query)
                else:
                    results = User.objects.all()

            if search == 'search_guide':
                section = "guide_request"
                resutls_model = 'user'
                if len(query) > 0:
                    results = User.objects.annotate(search=SearchVector('username', 'first_name', 'last_name'),).filter(search=query, mentorsetting__active=True)
                else:
                    results = User.objects.filter(mentorsetting__active=True)


    how_many_in_a_page = 12
    results_paginator = Paginator(results, how_many_in_a_page)
    page = request.GET.get('page')
    try:
        results = results_paginator.page(page)
    except PageNotAnInteger:
        results = results_paginator.page(1)
    except EmptyPage:
        results = results_paginator.page(results_paginator.num_pages)

    get_copy = request.GET.copy()
    params = get_copy.pop('page', True) and get_copy.urlencode()
    
    
    context = {
        'resutls_model': resutls_model,
        'results': results,
        'query': query,
        "form": form,
        "page" : page,
        "search": search,
        "params":params,
        "section": section,
    }

    return render(request, 'article/search_objects.html', context)
        
                


def list_articles(request, tag_name=None):
    
    articles = Article.published.all()
    form = SearchForm()
    tag = None

    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        articles = articles.filter(tags__in=[tag]) 

    how_many_in_a_page = 12
    articles_paginator = Paginator(articles, how_many_in_a_page)
    page = request.GET.get('page')
    try:
        articles = articles_paginator.page(page)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    except EmptyPage:
        articles = articles_paginator.page(articles_paginator.num_pages)


    context = {
        "articles": articles,
        'page': page,
        "tag":tag,
        "section": "articles",
        "form":form,
    }

    return render(request, 'article/list_articles.html', context)


@login_required
def user_followings_articles(request):
    user = get_object_or_404(User, username=request.user.username)
    user_fls = user.following.all()

    if not user_fls.exists():
        return redirect('dashboard')

    articles = Article.published.filter(author__in=user_fls)
    how_many_in_a_page = 12
    articles_paginator = Paginator(articles, how_many_in_a_page)
    page = request.GET.get('page')
    try:
        articles = articles_paginator.page(page)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    except EmptyPage:
        articles = articles_paginator.page(articles_paginator.num_pages)


    context = {
        "articles": articles,
        'page': page,
    }

    return render(request, 'article/followings_articles.html', context)


def article_detail(request, title):
    article = get_object_or_404(Article, slug=title)
    if request.user != article.author:
        article = get_object_or_404(Article, slug=title, status='published')

    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        #comment posted
        comment_form = CreateCommentForm(data=request.POST)
        if comment_form.is_valid():
            # dont save comment yet
            new_comment = comment_form.save(commit=False)
            new_comment.article = article # assign article
            new_comment.user = request.user
            new_comment.save() # save comment

            action_verb_string = 'کاربر "{}" روی مقاله "{}" نظر ارسال کرد'.format(request.user.username, new_comment.article.title)
            create_action(request.user, action_verb_string, new_comment)

            messages.success(request, "نظر شما با موفقیت ارسال شد", extra_tags="alert alert-success")
            return redirect(article.get_absolute_url())

    else:
        comment_form = CreateCommentForm()


    context = {
        "article": article,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'article/article_detail.html', context)

@require_POST
@login_required
def ajax_vote_actions(request):
    data = {'status': 'ko'}

    if request.is_ajax():
        id = request.POST.get('id')
        action = request.POST.get('action')
        
        data.update(message="قبل if action and article_id")
        if action and id:
            try:
                data.update(message="توی try")
                # 
                article_to_modify = Article.objects.get(id=id)
                print(article_to_modify)
                data.update(message="مقاله رو گرفتم")
                if action == "positive_vote":
                    already_negative_voted = \
                        request.user.articles_voted_negative.filter(id=article_to_modify.id)
                    data.update(message="بعد از already negative voted")
                    if already_negative_voted.exists():
                        article_to_modify.users_negative_vote.remove(request.user)
                    
                    article_to_modify.users_positive_vote.add(request.user)

                    action_verb_string = 'کاربر "{}" به مقاله "{}" رای داد'.format(request.user.username, article_to_modify.title[:30])
                    create_action(request.user, action_verb_string, article_to_modify)

                    data.update(status="ok")
                    data.update(message="رای مثبت شما ثبت شد")
                    return JsonResponse(data)

                if action == "negative_vote":
                    already_positive_voted = \
                        request.user.articles_voted_positive.filter(id=article_to_modify.id)
                        
                    data.update(message="بعد از already positive voted")
                    if already_positive_voted.exists():
                        article_to_modify.users_positive_vote.remove(request.user)
                    
                    article_to_modify.users_negative_vote.add(request.user)

                    action_verb_string = 'کاربر "{}" به مقاله "{}" رای داد'.format(request.user.username, article_to_modify.title[:30])
                    create_action(request.user, action_verb_string, article_to_modify)

                    data.update(status="ok")
                    data.update(message="رای منفی شما ثبت شد")
                    return JsonResponse(data)
                return JsonResponse(data)
                        

            except Article.DoesNotExist:
                data.update(message="توی قسمت اکسپت")
                return JsonResponse(data)
    
    data.update(message="قبل آخرین جیسون ریسپانس")
    return JsonResponse(data)
