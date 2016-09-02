from django.conf.urls import url
from apps.api.views import (
    TicketsRetrieveUpdateDestroyAPIView, TicketsCreateAPIView,
    BarcodesImportAPIView, MailchimpListsAPIView,
    MailchimpSubscriberAPIView, MailchimpCampaignAPIView,
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
    url(r'^mailchimp/lists/$',
        MailchimpListsAPIView.as_view(),
        name='mailchimp-lists'),
    url(r'^mailchimp/members/$',
        MailchimpSubscriberAPIView.as_view(),
        name='mailchimp-subscriber'),
    url(r'^mailchimp/campaigns/$',
        MailchimpCampaignAPIView.as_view(),
        name='mailchimp-campaign'),
]
