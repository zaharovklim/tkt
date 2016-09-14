import tempfile
import datetime

from django.contrib.auth.models import Group, User
from django.utils.encoding import force_text
from django.utils import timezone

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from import_export.formats import base_formats
from import_export.resources import modelresource_factory

from conf.settings import ROLES
from apps.tickets.models import Article
from apps.home.models import Barcode
from apps.bids.models import Bid, Buyer, Order

from .serializers import ArticlesSerializer, MerchantsSerializer
from .forms import BidForm, BuyerForm
from .constants import RESULT_CODES


class IsMerchant(permissions.BasePermission):

    def has_permission(self, request, view):
        merchant_group = Group.objects.get(name=ROLES.MERCHANT.value)
        user_groups = request.user.groups.all()

        return merchant_group in user_groups


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        admin_group = Group.objects.get(name=ROLES.ADMIN.value)
        user_groups = request.user.groups.all()

        return admin_group in user_groups


class ArticlesCreateAPIView(CreateAPIView):

    permission_classes = (IsMerchant, )
    serializer_class = ArticlesSerializer


class ArticlesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsMerchant, )
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer


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

    def post(self, request, *args, **kwargs):
        response = {}

        bid_form = BidForm(self.request.data)
        buyer_form = BuyerForm(self.request.data)

        if not bid_form.is_valid() or not buyer_form.is_valid():
            response = {
                "result": RESULT_CODES.INVALID_PARAMETER.value,
                "retry": True,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        buyer, created = Buyer.objects.get_or_create(
            email=buyer_form.cleaned_data['email']
        )
        buyer.firstname = buyer_form.cleaned_data['firstname']
        buyer.lastname = buyer_form.cleaned_data['lastname']
        buyer.save()

        article = bid_form.cleaned_data['article']
        number_of_tickets = bid_form.cleaned_data['number_of_tickets']

        # --------------------------------------------------------------------
        # Get bid_attempts counter
        bid_counting_timeframe = timezone.now() - datetime.timedelta(minutes=30)
        latest_bids_attmpts_count = Bid.objects.filter(
            buyer=buyer,
            article=article,
            created_at__gte=bid_counting_timeframe
        ).count()

        # --------------------------------------------------------------------
        # Validate Article's bid restriction for maximum attempts
        if latest_bids_attmpts_count > article.max_bid_attempts:
            response = {
                "result": RESULT_CODES.TOO_MANY_BIDS.value,
                "retry": False,
            }
            return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # --------------------------------------------------------------------
        bid_price = bid_form.cleaned_data['bid_price']

        bid = Bid.objects.create(
            buyer=buyer,
            article=article,
            bid_price=bid_price,
            number_of_tickets=number_of_tickets,
        )

        if bid_price > article.min_accepted_bid:
            bid_status = Bid.ACCEPTED
            response_status = status.HTTP_201_CREATED
            response = {
                "result": RESULT_CODES.WON_THE_BID.value,
                "retry": False,
                "bid_id": bid.id,
            }
        else:
            bid_status = Bid.REJECTED
            response_status = status.HTTP_200_OK
            response = {
                "result": RESULT_CODES.LOST_THE_BID.value,
                "retry": True,
                "bid_id": bid.id,
            }

        bid.status = bid_status
        bid.save()

        if bid_status is Bid.ACCEPTED:
            Order.objects.create(
                bid=bid,
            )

        return Response(response, status=response_status)


class MerchantAPIListView(ListAPIView):

    permission_classes = (IsAdmin, )

    queryset = User.objects.merchants()
    serializer_class = MerchantsSerializer
