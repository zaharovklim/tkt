from django.contrib.auth.models import Group
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from conf.settings import MERCHANT_GROUP_NAME
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView
)
from apps.home.models import (
    Ticket, Barcode
)
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TicketsSerializer
from import_export.formats import base_formats
from import_export.resources import modelresource_factory
import tempfile

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

    def get_import_formats(self):
        return [f for f in self.formats if f().can_import()]

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
        import_formats = self.get_import_formats()
        input_format = import_formats[
            int(self.request.POST['input_format'])
        ]()
        with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
            for chunk in data.chunks():
                uploaded_file.write(chunk)
        import_file = open(uploaded_file.name, input_format.get_read_mode())
        data = import_file.read()
        if not input_format.is_binary() and self.from_encoding:
            data = force_text(data, self.from_encoding)

        dataset = input_format.create_dataset(data)
        resource.import_data(dataset, dry_run=False,
                                      raise_errors=True)

        import_file.close()

        return Response(status=201)