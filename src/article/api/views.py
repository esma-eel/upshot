from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.decorators import action
from article.models import Article, Comment
from .serializers import ArticleModelSerializer, CommentModelSerializer
from .filters import ArticleFilterSet, CommentFilterSet


class ArticleModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    queryset = Article.objects.all().order_by("-created")
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ArticleFilterSet
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_permissions(self):
        return super().get_permissions()

    # default actions
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        article_object = serializer.save(author=self.request.user)
        return article_object

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # /end
    # custom actions
    @action(detail=True, methods=["post"], url_path="vote-positive")
    def vote_positive(self, request, *args, **kwargs):
        article_object = self.get_object()
        already_negative_voted = request.user.articles_voted_negative.filter(
            id=article_object.id
        )

        if already_negative_voted.exists():
            article_object.users_negative_vote.remove(request.user)

        article_object.users_positive_vote.add(request.user)

        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="vote-negative")
    def vote_negative(self, request, *args, **kwargs):
        article_object = self.get_object()
        already_positive_voted = request.user.articles_voted_positive.filter(
            id=article_object.id
        )

        if already_positive_voted.exists():
            article_object.users_positive_vote.remove(request.user)

        article_object.users_negative_vote.add(request.user)

        return Response({}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="following",
        permission_classes=[IsAuthenticated],
    )
    def get_following_users_articles(self, request, *args, **kwargs):
        user = request.user
        user_fls = user.following.all()
        if not user_fls.exists():
            return Response(
                {"message": "شما کسی را دنبال نمی‌کنید"},
                status=status.HTTP_200_OK,
            )

        queryset = self.get_queryset()
        fls_queryset = queryset.filter(author__in=user_fls)
        page = self.paginate_queryset(fls_queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(fls_queryset, many=True)
        return Response(serializer.data, staus=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="comments")
    def get_comments_list(self, request, *args, **kwargs):
        article_object = self.get_object()
        comments = article_object.comments.filter(active=True)
        page = self.paginate_queryset(comments)
        if page is not None:
            comment_serializer = CommentModelSerializer(page, many=True)
            return self.get_paginated_response(comment_serializer.data)

        comment_serializer = CommentModelSerializer(comments, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    # /end


class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilterSet

    def perform_create(self, serializer):
        comment_object = serializer.save(user=self.request.user)
        return comment_object
