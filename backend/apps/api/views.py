import tempfile
import requests
import json
import hashlib as hl
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from django.contrib.auth.models import Group
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from import_export.formats import base_formats
from import_export.resources import modelresource_factory

from conf.settings import MERCHANT_GROUP_NAME, MAILCHIMP_API_KEY, MAILCHIMP_URL
from apps.tickets.models import Ticket
from .serializers import TicketsSerializer
from apps.home.models import Barcode


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


class MailchimpRequest(object):

    def send_request(self, uri, params, method='GET'):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        endpoint = urlparse.urljoin(MAILCHIMP_URL, uri)

        if method == 'POST':
            response = requests.post(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    data=json.dumps(params))
        if method == 'PATCH':
            response = requests.patch(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                     data=json.dumps(params))
        if method == 'DELETE':
            response = requests.delete(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    data=json.dumps(params))
        else:
            response = requests.get(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    params=params, verify=False)

        try:
            response.raise_for_status()
            body = response.json()
        except:
            return Response('Invalid request', status.HTTP_400_BAD_REQUEST)

        return body


class MailchimpListsAPIView(APIView, MailchimpRequest):

    def get(self, *args, **kwargs):
        return Response(self.get_lists(), status=status.HTTP_200_OK)

    def get_lists(self):
        uri = 'lists'
        params =   {
            'fields': 'lists.id,lists.name,lists.stats.member_count',
        }
        response = self.send_request(uri, params)

        return response


class MailchimpSubscriberAPIView(APIView, MailchimpRequest):

    def get_subscriber(self, list_id, email_md5):
        uri = 'lists/{}/members/{}'.format(list_id, email_md5)
        params = {
            'fields': 'id,email_address,status,\
                merge_fields.LNAME,merge_fields.FNAME',
        }
        response = self.send_request(uri, params)

        return response

    def add_subscriber(self, list_id):
        uri = 'lists/{}/members/'.format(list_id)
        params = { 'email_address': self.request.POST['email'],
                   'merge_fields':  {
                                      'FNAME': self.request.POST['fname'],
                                      'LNAME': self.request.POST['lname']
                                    },
                   'status': 'subscribed',
                   }
        response = self.send_request(uri, params, method='POST')

        return response

    def update_subscriber(self, list_id, email_md5):
        uri = 'lists/{}/members/{}'.format(list_id, email_md5)
        params = dict(self.request.data._iteritems())
        response = self.send_request(uri, params, method='PATCH')

        return response

    def retrive_list(self):
        mail_lists = MailchimpListsAPIView.get_lists(self)

        if self.request.method == 'GET':
            list_name = self.request.GET.get('list_name')
        else:
            list_name = self.request.data['list_name']

        for mail_list in mail_lists['lists']:
            if list_name in mail_list['name']:
                list_id = mail_list['id']
        return list_id

    def get(self, *args, **kwargs):
        em_md5 = hl.md5(self.request.GET['email'].encode('utf-8')).hexdigest()

        list_id = self.retrive_list()

        try:
            list_id
            user_info = self.get_subscriber(list_id, em_md5)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):

        list_id = self.retrive_list()

        try:
            list_id
            user_info = self.add_subscriber(list_id)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        em_md5 = hl.md5(self.request.data['email'].encode('utf-8')).hexdigest()

        list_id = self.retrive_list()

        try:
            list_id
            user_info = self.update_subscriber(list_id, em_md5)
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)


class MailchimpCampaignAPIView(APIView, MailchimpRequest):

    def create_campaign(self):
        uri = 'campaigns'
        params = {
            'type': self.request.POST['type'],
            'settings': {
                'subject_line': self.request.POST['subject'],
                'from_name': self.request.POST['from'],
                'reply_to': self.request.POST['reply_to'],
            }
        }
        response = self.send_request(uri, params)

        return response

    def get_campaign(self):
        uri = 'campaigns'
        params = { 'fields': 'campaigns.id,campaigns.status,campaigns.type,campaigns.recipients,campaigns.settings' }
        response = self.send_request(uri, params)

        return response

    def get(self, *args, **kwargs):
        try:
            user_info = self.get_campaign()
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):

        try:
            user_info = self.create_campaign()
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)


class MailchimpCampaignActionAPIView(APIView, MailchimpRequest):

    def create_campaign(self):
        uri = 'campaigns'
        params = {
            'type': self.request.POST['type'],
            'settings': {
                'subject_line': self.request.POST['subject'],
                'from_name': self.request.POST['from'],
                'reply_to': self.request.POST['reply_to'],
            }
        }
        response = self.send_request(uri, params)

        return response

    def get_campaign(self):
        uri = 'campaigns'
        params = { 'fields': 'campaigns.id,campaigns.status,campaigns.type,campaigns.recipients,campaigns.settings' }
        response = self.send_request(uri, params)

        return response

    def get(self, *args, **kwargs):
        if self.request.get_full_path():
            print(self.request.get_full_path())
        else:
            try:
                user_info = self.get_campaign()
                return Response(user_info, status=status.HTTP_200_OK)
            except NameError:
                return Response('No list with that name found',
                                status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):

        try:
            user_info = self.create_campaign()
            return Response(user_info, status=status.HTTP_200_OK)
        except NameError:
            return Response('No list with that name found',
                            status=status.HTTP_400_BAD_REQUEST)


