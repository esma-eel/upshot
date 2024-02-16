from rest_framework import serializers
from upshot.actions.models import Action


class ActionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        exclude = []
