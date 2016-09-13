from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

from conf.settings import ROLES
from apps.tickets.models import Article
from apps.home.models import Widget


@staff_member_required
def bid_statistics_overall_view(request):
    admin_group = Group.objects.get(name=ROLES.ADMIN.value)
    if admin_group not in request.user.groups.all():
        return HttpResponseForbidden(
            "Only admin has permission to overall statistics"
        )

    objects = Widget.objects.all()
    overall_statistics = {'accepted': 0, 'paid': 0, 'rejected': 0}
    for object in objects:
        for stat_prop in object.bid_statistics.keys():
            overall_statistics[stat_prop] += object.bid_statistics[stat_prop]

    context = {
        'objects': ({
            'id': 1,
            'name': 'Overall',
            'bid_statistics': overall_statistics,
        }, )
    }
    context['model'] = 'Overall'
    return render(request, 'statistics/statistics_per_model.html', context)


@staff_member_required
def bid_statistics_per_model_view(request, model):
    STATISTICS_MODELS_MAP = {
        'merchant': User,
        'widget': Widget,
        'ticket': Article,
    }

    objects = (
        STATISTICS_MODELS_MAP[model].objects
        .get_objects_list_by_role(request.user)
    )

    context = {
        'objects': objects,
        'model': model,
    }
    return render(request, 'statistics/statistics_per_model.html', context)
