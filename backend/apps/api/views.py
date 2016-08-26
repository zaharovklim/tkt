from django.contrib.auth.models import Group
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView
)
from rest_framework import permissions

from conf.settings import MERCHANT_GROUP_NAME

from apps.home.models import Ticket

from .serializers import TicketsSerializer


class IsMerchant(permissions.BasePermission):

    def has_permission(self, request, view):
        merchant_group = Group.objects.get(name=MERCHANT_GROUP_NAME)
        user_groups = request.user.groups.all()

        return merchant_group in user_groups


class TicketsCreateAPIView(CreateAPIView):

    permission_classes = (IsMerchant, )
    serializer_class = TicketsSerializer


class TicketsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsMerchant, )
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer
