from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/statistics/', include('apps.statistics.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('apps.api.urls')),
    url(r'^', include('apps.home.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
