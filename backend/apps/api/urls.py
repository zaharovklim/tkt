from django.conf.urls import url
from apps.api.views import (
    TicketsRetrieveUpdateDestroyAPIView, TicketsCreateAPIView
)


urlpatterns = [
    url(r'^tickets/$',
        TicketsCreateAPIView.as_view(),
        name='tickets-create'),
    url(r'^tickets/(?P<pk>[\d]+)/$',
        TicketsRetrieveUpdateDestroyAPIView.as_view(),
        name='tickets')
]
