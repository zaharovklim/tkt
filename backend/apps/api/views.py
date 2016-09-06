import tempfile
import hashlib as hl
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from django.contrib.auth.models import Group
from django.utils.encoding import force_text

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from .mailchimp_api import *

from conf.settings import ROLES
from apps.tickets.models import Ticket
from apps.home.models import Barcode

from .serializers import TicketsSerializer


class IsMerchant(permissions.BasePermission):

    def has_permission(self, request, view):
        merchant_group = Group.objects.get(name=ROLES.MERCHANT.value)
        user_groups = request.user.groups.all()

        return merchant_group in user_groups


class TicketsCreateAPIView(CreateAPIView):

    permission_classes = (IsMerchant, )
    serializer_class = TicketsSerializer


class TicketsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsMerchant, )
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer


class BarcodesImportAPIView(APIView):

    permission_classes = (IsMerchant, )
    model = Barcode
    from_encoding = "utf-8"

    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    resource_class = None

    def get_import_formats(self, format):
        return [f for f in self.formats if format in f().get_title()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        return self.get_resource_class()

    def put(self, *args, **kwargs):
        data = self.request.FILES['import_file_name']
        resource = self.get_import_resource_class()()
        input_format = self.get_import_formats(
            str(self.request.POST['input_format']).lower()
        )[0]()
        with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
            for chunk in data.chunks():
                uploaded_file.write(chunk)
        import_file = open(uploaded_file.name, input_format.get_read_mode())
        data = import_file.read()
        if not input_format.is_binary() and self.from_encoding:
            data = force_text(data, self.from_encoding)

        dataset = input_format.create_dataset(data)
        resource.import_data(dataset, dry_run=False, raise_errors=True)

        import_file.close()

        return Response(status=status.HTTP_201_CREATED)


class MailchimpListsAPIView(APIView):

    def get(self, *args, **kwargs):
        return Response(MailchimpList.get_lists(self.request), status=status.HTTP_200_OK)


class MailchimpSubscriberAPIView(APIView):

    def get(self, *args, **kwargs):
        em_md5 = hl.md5(self.request.GET['email'].encode('utf-8')).hexdigest()

        list_id = MailchimpSubscriber.retrive_list(self.request)

        try:
            list_id
            user_info = MailchimpSubscriber.get_subscriber(list_id, em_md5)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No lists with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        list_id = MailchimpSubscriber.retrive_list(self.request)

        try:
            list_id
            user_info = MailchimpSubscriber.add_subscriber(self.request, list_id)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No lists with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        em_md5 = hl.md5(self.request.data['email'].encode('utf-8')).hexdigest()

        list_id = MailchimpSubscriber.retrive_list(self.request)

        try:
            list_id
            user_info = MailchimpSubscriber.update_subscriber(self.request, list_id, em_md5)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No lists with that name found',
                            status=status.HTTP_400_BAD_REQUEST)


class MailchimpCampaignAPIView(APIView):

    def get(self, *args, **kwargs):
        try:
            user_info = MailchimpCampaign.get_campaign(self.request)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No lists with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        try:
            user_info = MailchimpCampaign.create_campaign(self.request)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No lists with that name found',
                            status=status.HTTP_400_BAD_REQUEST)
