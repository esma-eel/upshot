from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from article.models import Article, Comment


class ArticleModelSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    users_positive_vote = serializers.SerializerMethodField()
    users_negative_vote = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = []
        read_only_fields = [
            "users_positive_vote",
            "created",
            "updated",
            "users_negative_vote",
            "author",
        ]

    def get_users_positive_vote(self, obj):
        return obj.users_positive_vote.count()

    def get_users_negative_vote(self, obj):
        return obj.users_negative_vote.count()


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exlcude = []
        read_only_fields = ["created", "updated", "active"]
