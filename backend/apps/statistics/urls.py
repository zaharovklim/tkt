from django.conf.urls import url

from .views import bid_statistics_overall_view, bid_statistics_per_model_view


urlpatterns = [
    url(
        r'^overall/$',
        bid_statistics_overall_view,
        name='statistics_overall'
    ),
    url(
        r'^(?P<model>\w+)/$',
        bid_statistics_per_model_view,
        name='statistics_per_model'
    ),
]
