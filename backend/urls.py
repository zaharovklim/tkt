from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME


urlpatterns = [
    url(r'^admin/statistics/', include('apps.statistics.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('apps.api.urls')),
    url(r'^', include('apps.home.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
