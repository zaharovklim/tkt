from django.conf.urls import url
from apps.api.views import (
    ArticlesRetrieveUpdateDestroyAPIView, ArticlesCreateAPIView,
    BarcodesImportAPIView, BidAPIView, MerchantAPIListView,
    MerchantsWidgetsAPIListView, WidgetArticlesRetrieveAPIView,
)


urlpatterns = [
    url(r'^articles/$',
        ArticlesCreateAPIView.as_view(),
        name='articles-create'),
    url(r'^articles/(?P<pk>[\d]+)/$',
        ArticlesRetrieveUpdateDestroyAPIView.as_view(),
        name='articles'),
    url(r'^barcodes/import/$',
        BarcodesImportAPIView.as_view(),
        name='barcodes-import'),
    url(r'^bid/$',
        BidAPIView.as_view(),
        name='bid'),
    url(r'^merchants/$',
        MerchantAPIListView.as_view(),
        name='merchants'),
    url(r'^merchants/widgets/$',
        MerchantsWidgetsAPIListView.as_view(),
        name='merchants-widgets'),
    url(r'^widget/(?P<pk>[\d]+)/articles/$',
        WidgetArticlesRetrieveAPIView.as_view(),
        name='widget-articles'),
]
