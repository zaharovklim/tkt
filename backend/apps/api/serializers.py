from rest_framework import serializers

from apps.tickets.models import Ticket


class TicketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
