from rest_framework import serializers

from django.contrib.auth.models import User

from apps.tickets.models import Article


class ArticlesSerializer(serializers.ModelSerializer):

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article


class MerchantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
