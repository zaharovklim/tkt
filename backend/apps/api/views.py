from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView
)

from apps.home.models import Ticket

from .serializers import TicketsSerializer


class TicketsCreateAPIView(CreateAPIView):

    serializer_class = TicketsSerializer


class TicketsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer
