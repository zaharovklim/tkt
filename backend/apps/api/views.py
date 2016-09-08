import tempfile

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

from conf.settings import ROLES
from apps.tickets.models import Ticket
from apps.home.models import Barcode
from apps.bids.models import Bid

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


class BidAPIView(APIView):

    def post(self, r, *args, **kwargs):
        context = {}

        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # --------------------------------------------------------------------
        # Get and clean ticket_id, bid_price and number_of_tickets
        try:
            ticket_id = int(self.request.data.get('ticket_id'))
        except (ValueError, TypeError):
            return Response("Ticket id is invalid")

        try:
            bid_price = float(self.request.data.get('bid_price'))
        except (ValueError, TypeError):
            return Response("Bid price is invalid")

        try:
            number_of_tickets = int(self.request.data.get('number_of_tickets'))
        except (ValueError, TypeError):
            return Response("Number of tickets is invalid")

        # --------------------------------------------------------------------
        # Increment bid_attempts counter
        if self.request.session.get('bid_attempts') is None:
            self.request.session['bid_attempts'] = 1
        else:
            self.request.session['bid_attempts'] += 1
        bid_attempts = self.request.session['bid_attempts']

        # --------------------------------------------------------------------
        # Select and test for existence of Ticket user trying to bid
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response("Ticket does not exist")

        # --------------------------------------------------------------------
        # Validate Ticket's bid restriction for maximum attempts
        if bid_attempts > ticket.max_bid_attempts:
            return Response(
                "Bid attempts have exceeded maximum for this ticket"
            )

        # --------------------------------------------------------------------
        bid_status = Bid.REJECTED
        response = "You lose"
        if bid_price > ticket.min_accepted_bid:
            bid_status = Bid.ACCEPTED
            response = "You won"

        # TODO: offer to user fill the order form
        context['reponse'] = response

        Bid.objects.create(
            session_key=self.request.session.session_key,
            ticket=ticket,
            bid_price=bid_price,
            number_of_tickets=number_of_tickets,
            status=bid_status,
        )

        return Response(response)
