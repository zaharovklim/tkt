from rest_framework import serializers

from apps.tickets.models import Article


class TicketsSerializer(serializers.ModelSerializer):

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Article
