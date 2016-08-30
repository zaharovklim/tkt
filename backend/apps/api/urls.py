from django.conf.urls import url
from apps.api.views import (
    TicketsRetrieveUpdateDestroyAPIView, TicketsCreateAPIView, BarcodesImportAPIView
)


urlpatterns = [
    url(r'^tickets/$',
        TicketsCreateAPIView.as_view(),
        name='tickets-create'),
    url(r'^tickets/(?P<pk>[\d]+)/$',
        TicketsRetrieveUpdateDestroyAPIView.as_view(),
        name='tickets'),
    url(r'^barcodes/import/$',
        BarcodesImportAPIView.as_view(),
        name='barcodes-import'),
]
