from rest_framework import serializers

from apps.home.models import Ticket


class TicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
