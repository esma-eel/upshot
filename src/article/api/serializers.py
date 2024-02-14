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
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if self.instance:
            # update
            for create_only_field in self.Meta.create_only_fields:
                if create_only_field in data.keys():
                    data.pop(create_only_field)
        return data

    class Meta:
        model = Comment
        exclude = []
        read_only_fields = ["created", "updated", "user"]
        create_only_fields = ["article"]
