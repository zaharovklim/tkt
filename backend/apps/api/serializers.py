from rest_framework import serializers

from django.contrib.auth.models import User

from apps.tickets.models import Article
from apps.home.models import Widget


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


class WidgetSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'widget_type')
        model = Widget


class MerchantsWidgetsSerializer(serializers.ModelSerializer):

    widgets = WidgetSerializer(source="widget_set", many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'widgets',
        )


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'description', 'box_office_price')
        model = Article


class WidgetArticlesSerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(source="article_set", many=True)

    class Meta:
        fields = ('articles', )
        model = Widget
