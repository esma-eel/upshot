from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from upshot.actions.models import Action
from upshot.actions.utils import create_action
from upshot.article.forms import ArticleCreateEditForm
from upshot.article.models import Article, Comment
from upshot.mentor.forms import MentorSettingForm
from upshot.mentor.models import MentorRequest, MentorSetting

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from upshot.profiles.models import Profile
from upshot.account.models import Contact


def user_registration(request):
    """
    Register user
    """
    # check if user already registered and logged in
    if request.user.is_authenticated:
        messages.warning(
            request,
            "شما قبلا ثبت نام کرده اید",
            extra_tags="alert alert-warning",
        )
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]

            grade = form.cleaned_data["grade"]
            student_number = form.cleaned_data["student_number"]

            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            Profile.objects.create(
                user=user, student_number=student_number, grade=grade
            )
            action_verb_string = 'کاربر "{}" یک حساب ایجاد کرد'.format(
                user.username
            )
            create_action(user, action_verb_string, user)
            MentorSetting.objects.create(user=user)

            messages.success(
                request,
                "حساب کاربری شما با نام کاربری {} با موفقیت ایجاد شد".format(
                    user.username
                ),
                extra_tags="alert alert-success",
            )
            return redirect("login")

    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


@login_required
def dashboard(request):
    """ "
    Users main dashboard page
    """
    # display all actions
    actions = None
    # get id of people who users is following
    following_ids = request.user.following.values_list("id", flat=True)
    # get count of comments of all articles which user authored
    user_articles_comments_count = Comment.objects.filter(
        article__author=request.user
    ).count()
    # followers count
    user_followers_count = request.user.followers.count()
    # following count
    user_followings_count = request.user.following.count()
    # published articles count
    user_published_articles_count = Article.published.filter(
        author=request.user
    ).count()

    # get actions of users who you follow or if ur admin you get all users
    all_users_except_request_user = User.objects.exclude(id=request.user.id)
    requested_user_actions = Action.objects.exclude(
        user__in=all_users_except_request_user
    )[:5]

    if following_ids:
        # only get followings actions
        actions = Action.objects.exclude(user=request.user)
        actions = actions.filter(user__id__in=following_ids)
        actions = actions.select_related("user", "user__profile")[:5]

    # normal actions = actions[:5]
    # more advance actions
    # every thing that is related to the followings will be shown here
    # actions = actions.select_related('user', 'user__profile')
    # .prefetch_related('target')[:5]

    context = {
        "actions": actions,
        "user_articles_comments_count": user_articles_comments_count,
        "user_followers_count": user_followers_count,
        "user_followings_count": user_followings_count,
        "user_published_articles_count": user_published_articles_count,
        "requested_user_actions": requested_user_actions,
    }
    return render(request, "account/dashboard.html", context)


@login_required
def profile_edit(request):
    """
    Edit users profile
    """
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            action_verb_string = 'کاربر "{}" حساب خود را ویرایش کرد'.format(
                request.user.username
            )
            create_action(request.user, action_verb_string, request.user)

            messages.success(
                request,
                "حساب کاربری شما با موفقیت ویرایش شد",
                extra_tags="alert alert-success",
            )

        else:
            # this part manages errors
            # couse we used modelForms we have to handle form errors like this
            all_errors = user_form.errors
            all_errors.update(profile_form.errors)
            if all_errors:
                for key, val in all_errors.items():
                    for error_text in val:
                        messages.error(
                            request, error_text, extra_tags="alert alert-danger"
                        )

            return redirect("profile_edit")

        return redirect("dashboard")

    else:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

        if not profile:
            Profile.objects.create(user=request.user)
            action_verb_string = 'کاربر "{}" یک حساب ایجاد کرد'.format(
                request.user.username
            )
            create_action(request.user, action_verb_string, request.user)

        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "section": "profile",
    }

    return render(request, "account/profile_edit.html", context)


@login_required
def mentor_setting(request):
    """
    Mentor setting of user
    """
    if request.method == "POST":
        form = MentorSettingForm(
            instance=request.user.mentorsetting, data=request.POST
        )

        if form.is_valid():
            form.save()

            action_verb_string = (
                'کاربر "{}" تنظیمات راهنمایی خود را ویرایش کرد'.format(
                    request.user.username
                )
            )
            create_action(
                request.user, action_verb_string, request.user.mentorsetting
            )

            messages.success(
                request,
                "تنظیمات راهنمایی شما با موفقیت ویرایش شد",
                extra_tags="alert alert-success",
            )

        else:
            # this part manages errors
            # couse we used modelForms we have to handle form errors like this
            all_errors = form.errors
            if all_errors:
                for key, val in all_errors.items():
                    for error_text in val:
                        messages.error(
                            request, error_text, extra_tags="alert alert-danger"
                        )

            return redirect("mentor_setting")

        return redirect("dashboard")

    else:
        try:
            user_mentor_setting = MentorSetting.objects.get(user=request.user)
        except MentorSetting.DoesNotExist:
            user_mentor_setting = None

        if not user_mentor_setting:
            MentorSetting.objects.create(user=request.user)

        form = MentorSettingForm(
            instance=request.user.mentorsetting,
            initial={"active": int(request.user.mentorsetting.active)},
        )

    context = {
        "form": form,
        "section": "profile",
    }

    return render(request, "account/mentor_setting.html", context)


def user_profile(request, username):
    """
    Show users porfile
    """
    user_original = get_object_or_404(User, username=username)

    try:
        profile = Profile.objects.get(user=user_original)
    except Profile.DoesNotExist:
        profile = None

    if not profile:
        Profile.objects.create(user=user_original)
        action_verb_string = 'کاربر "{}" یک حساب ایجاد کرد'.format(
            user_original.username
        )
        create_action(user_original, action_verb_string, user_original)

    profile = {
        "grade": user_original.profile.get_grade_display(),
        "photo": user_original.profile.photo,
        "about": user_original.profile.about,
    }

    user_articles = Article.published.filter(author=user_original)
    # pagination of user articles
    how_many_in_a_page = 12
    user_articles_paginator = Paginator(user_articles, how_many_in_a_page)
    page = request.GET.get("page")
    try:
        user_articles = user_articles_paginator.page(page)
    except PageNotAnInteger:
        user_articles = user_articles_paginator.page(1)
    except EmptyPage:
        user_articles = user_articles_paginator.page(
            user_articles_paginator.num_pages
        )

    context = {
        "user": user_original,
        "profile": profile,
        "user_articles": user_articles,
    }
    return render(request, "account/user_profile.html", context)


@login_required
def user_followers_management(request):
    """
    Mange users followers
    """
    user = get_object_or_404(User, username=request.user.username)
    followers_list = user.followers.all()

    context = {"followers": followers_list, "section": "follower_following"}
    return render(request, "account/followers_management.html", context)


@login_required
def user_followings_management(request):
    """
    Manage users followings
    """
    user = get_object_or_404(User, username=request.user.username)
    followings_list = user.following.all()

    context = {"followings": followings_list, "section": "follower_following"}
    return render(request, "account/followings_management.html", context)


@require_POST
@login_required
def ajax_follow_unfollow(request):
    """
    Follow/Unfollow others with ajax request
    """
    data = {"status": "ko"}

    if request.is_ajax():
        id = request.POST.get("id")
        action = request.POST.get("action")
        if action and id:
            try:
                user_to_action = User.objects.get(id=id)
                if action == "delete_follower":
                    Contact.objects.filter(
                        user_from=user_to_action, user_to=request.user
                    ).delete()
                    data.update(status="ok")
                    data.update(
                        message="کاربر {} از دنبال کنندگان شما حذف شد".format(
                            user_to_action.username
                        )
                    )
                    return JsonResponse(data)

                if (
                    action == "follow_user"
                    and request.user.id != user_to_action.id
                ):
                    Contact.objects.get_or_create(
                        user_from=request.user, user_to=user_to_action
                    )

                    action_verb_string = (
                        'کاربر "{}" کاربر "{}" را دنبال میکند'.format(
                            request.user, user_to_action
                        )
                    )
                    create_action(
                        request.user, action_verb_string, user_to_action
                    )

                    data.update(status="ok")
                    data.update(
                        message="شما کاربر {} را دنبال میکنید".format(
                            user_to_action.username
                        )
                    )
                    return JsonResponse(data)

                if action == "unfollow_user" or "delete_following":
                    Contact.objects.filter(
                        user_from=request.user, user_to=user_to_action
                    ).delete()
                    data.update(status="ok")
                    data.update(
                        message="شما کاربر {} را دنبال نمیکنید".format(
                            user_to_action.username
                        )
                    )
                    return JsonResponse(data)

            except User.DoesNotExist:
                return JsonResponse(data)

    return JsonResponse(data)


@login_required
def user_articles_management(request):
    """
    Dashboard page to mangae authored articles
    """
    articles = Article.objects.filter(author=request.user)

    context = {"articles": articles, "section": "article"}

    return render(request, "account/articles_management.html", context)


@require_POST
@login_required
def ajax_article_actions(request):
    """
    Delete action of article with ajax call
    """
    data = {"status": "ko"}

    if request.is_ajax():
        id = request.POST.get("id")
        action = request.POST.get("action")
        if action and id:
            try:
                article_to_modify = Article.objects.get(id=id)
                if action == "delete_article":
                    data.update(status="ok")
                    data.update(
                        message=(
                            "مقاله {} با موفقیت از مقالات شما حذف شد.".format(
                                article_to_modify.title
                            )
                        )
                    )

                    article_to_modify.delete()
                    return JsonResponse(data)

            except Article.DoesNotExist:
                return JsonResponse(data)

    return JsonResponse(data)


@login_required
def create_article(request):
    """
    Author new article
    """
    if request.method == "POST":
        form = ArticleCreateEditForm(data=request.POST, files=request.FILES)
        if form.is_valid:
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.slug = slugify(new_article.title, allow_unicode=True)
            new_article.save()
            form.save_m2m()

            if new_article.status == "published":
                action_verb_string = (
                    'کاربر "{}" مقاله "{}" را ایجاد کرد'.format(
                        request.user.username, new_article.title
                    )
                )
                create_action(request.user, action_verb_string, new_article)

            messages.success(
                request,
                "مقاله شما با عنوان '{}' با موفقیت ایجاد شد".format(
                    new_article.title
                ),
                extra_tags="alert alert-success",
            )

            return redirect("articles_management")

    else:
        form = ArticleCreateEditForm()

    return render(
        request,
        "account/article_edit.html",
        context={"form": form, "section": "article"},
    )


@login_required
def edit_article(request, id):
    """
    Edit authored article
    """
    article = Article.objects.get(id=id)

    if request.method == "POST":
        form = ArticleCreateEditForm(
            instance=article, data=request.POST, files=request.FILES
        )
        if form.is_valid:
            new_article = form.save(commit=False)
            if not new_article.slug:
                new_article.slug = slugify(
                    new_article.title, allow_unicode=True
                )

            new_article.save()
            form.save_m2m()

            if new_article.status == "published":
                action_verb_string = (
                    'کاربر "{}" مقاله "{}" را منتشر کرد'.format(
                        request.user.username, new_article.title
                    )
                )
                create_action(request.user, action_verb_string, new_article)

            messages.success(
                request,
                "مقاله شما با عنوان '{}' با موفقیت ویرایش شد".format(
                    new_article.title
                ),
                extra_tags="alert alert-success",
            )

            return redirect("articles_management")

    else:
        form = ArticleCreateEditForm(instance=article)

    return render(
        request,
        "account/article_edit.html",
        context={
            "form": form,
            "section": "article",
            "title_edit": "title_edit",
        },
    )


@login_required
def user_sent_comments_management(request):
    """
    Dashboard page to get list of comments sent by user
    """
    comments = Comment.objects.filter(user=request.user).all()

    context = {"comments": comments, "section": "comment"}
    return render(request, "account/comments_sent_get_management.html", context)


@login_required
def user_get_comments_management(request):
    """
    Dashboard page to get list of comments on authored articles
    """
    user_articles_comments = Comment.objects.filter(
        article__author=request.user
    )

    context = {"comments": user_articles_comments, "section": "comment"}
    return render(request, "account/comments_sent_get_management.html", context)


@require_POST
@login_required
def ajax_comment_actions(request):
    """
    RUD actions on comments with ajax call
    """
    data = {"status": "ko"}

    if request.is_ajax():
        id = request.POST.get("id")
        action = request.POST.get("action")
        if action and id:
            try:
                comment_to_modify = Comment.objects.get(id=id)
                if (comment_to_modify.user == request.user) or (
                    comment_to_modify.article.author == request.user
                ):
                    user_can_do_thingns = True
                else:
                    user_can_do_thingns = False

                if action == "delete_comment" and user_can_do_thingns:
                    data.update(status="ok")
                    data.update(
                        message="نظر {} با موفقیت از نظرات شما حذف شد.".format(
                            comment_to_modify.body[:10]
                        )
                    )

                    comment_to_modify.delete()
                    return JsonResponse(data)

                if (action == "edit_comment_body") and (
                    request.user == comment_to_modify.user
                ):
                    body = request.POST.get("body")
                    data.update(status="ok")
                    data.update(
                        message="نظر شما از '{}' به '{}' تغییر یافت".format(
                            comment_to_modify.body[:15], body[:15]
                        )
                    )
                    comment_to_modify.body = body
                    comment_to_modify.save()

                    return JsonResponse(data)

                if action == "change_active_status" and user_can_do_thingns:
                    new_active_status = request.POST.get("active")

                    data.update(status="ok")
                    data.update(
                        message="نظر شما '{}' تغییر وضعیت یافت.".format(
                            comment_to_modify.body[:15],
                        )
                    )

                    if new_active_status == "True":
                        comment_to_modify.active = True
                    else:
                        comment_to_modify.active = False

                    comment_to_modify.save()

                    return JsonResponse(data)

            except Article.DoesNotExist:
                return JsonResponse(data)

    return JsonResponse(data)


@login_required
def user_sent_request_management(request):
    """
    List of mentor requests sent to others
    """
    user_sent_requests = MentorRequest.objects.filter(user_from=request.user)

    context = {
        "user_sent_requests": user_sent_requests,
        "section": "guide",
    }

    return render(request, "account/requests_sent_management.html", context)


@login_required
def user_inbox_request_management(request):
    """
    List of mentor requests to user
    """
    user_inbox_requests = MentorRequest.objects.filter(user_to=request.user)

    context = {
        "user_inbox_requests": user_inbox_requests,
        "section": "guide",
    }

    return render(request, "account/requests_inbox_management.html", context)


@require_POST
@login_required
def ajax_mentor_request_actions(request):
    """
    Manage mentor requests, sent/approve/reject mentor requests
    """
    data = {"status": "ko"}

    if request.is_ajax():
        id = request.POST.get("id")
        action = request.POST.get("action")
        if action and id:
            try:
                if action == "send_mentor_request":
                    user_to = User.objects.get(id=id)
                    qs = MentorRequest.objects.filter(
                        user_from=request.user, user_to=user_to
                    )

                    if qs.exists():
                        data.update(
                            message=(
                                "کاربر محترم شما تنها میتوانید یک درخواست"
                                " راهنمایی برای {} ارسال کنید".format(user_to)
                            )
                        )
                        return JsonResponse(data)

                    request_to_modify = MentorRequest.objects.create(
                        user_from=request.user, user_to=user_to
                    )

                    data.update(status="ok")
                    data.update(
                        message=(
                            "درخواست راهنمایی از طرف "
                            "{} به {} با موفقیت ارسال شد ".format(
                                request.user, request_to_modify.user_to
                            )
                        )
                    )

                    return JsonResponse(data)

                request_to_modify = MentorRequest.objects.get(id=id)

                if (request_to_modify.user_from == request.user) or (
                    request_to_modify.user_to == request.user
                ):
                    user_can_do_thingns = True
                else:
                    user_can_do_thingns = False

                if action == "delete_st_request" and user_can_do_thingns:
                    data.update(status="ok")
                    data.update(
                        message=(
                            "درخواست راهنمایی از طرف "
                            "{} به {} با موفقیت حذف شد".format(
                                request_to_modify.user_from,
                                request_to_modify.user_to,
                            )
                        )
                    )

                    request_to_modify.delete()
                    return JsonResponse(data)

                if (action == "mentor_accept_request") and (
                    request.user == request_to_modify.user_to
                ):
                    data.update(status="ok")
                    data.update(
                        message=(
                            "درخواست راهنمایی از طرف {} به "
                            "{} با موفقیت پذیرفته شد".format(
                                request_to_modify.user_from,
                                request_to_modify.user_to,
                            )
                        )
                    )

                    request_to_modify.approved = True
                    request_to_modify.save()

                    return JsonResponse(data)

                if (action == "mentor_reject_request") and (
                    request.user == request_to_modify.user_to
                ):
                    data.update(status="ok")
                    data.update(
                        message=(
                            "درخواست راهنمایی از طرف {}"
                            " به {} با موفقیت رد شد ".format(
                                request_to_modify.user_from,
                                request_to_modify.user_to,
                            )
                        )
                    )

                    request_to_modify.approved = False
                    request_to_modify.save()
                    return JsonResponse(data)

            except MentorRequest.DoesNotExist:
                return JsonResponse(data)

    return JsonResponse(data)
