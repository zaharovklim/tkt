from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden

from conf.settings import ADMIN_GROUP_NAME
from apps.tickets.models import Ticket
from apps.bids.models import Bid
from apps.home.models import Widget


def index(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    if request.method == 'POST':
        # Get and clean ticket_id and bid_price
        try:
            ticket_id = int(request.POST.get('ticket_id'))
        except ValueError:
            return HttpResponseBadRequest("Ticket id is invalid")

        try:
            bid_price = float(request.POST.get('bid_price'))
        except ValueError:
            return HttpResponseBadRequest("Bid price is invalid")

        # Increment bid_attempts counter
        if request.session.get('bid_attempts') is None:
            request.session['bid_attempts'] = 1
        else:
            request.session['bid_attempts'] += 1
        bid_attempts = request.session['bid_attempts']

        # Select and test for existence of Ticket user trying to bid
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return HttpResponseBadRequest("Ticket does not exist")

        # Validate Ticket's bid restriction for user
        if bid_attempts > ticket.max_bid_attempts:
            return HttpResponseBadRequest(
                "Bid attempts have exceeded maximum for this ticket"
            )
        if bid_price < ticket.min_accepted_bid:
            return HttpResponseBadRequest(
                "Bid price is not high enough"
            )

        # Check if current bid_price is higher than the last one
        if request.session['last_bid_price'] > bid_price:
            return HttpResponseBadRequest(
                "Bid price should be higher than the last one"
            )
        request.session['last_bid_price'] = bid_price

        Bid.objects.create(
            session_key=request.session.session_key,
            ticket=ticket,
            bid_price=bid_price,
        )

    return render(request, 'home/index.html')


@staff_member_required
def bid_statistics_overall_view(request):
    admin_group = Group.objects.get(name=ADMIN_GROUP_NAME)
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
    return render(request, 'home/statistics_per_model.html', context)


@staff_member_required
def bid_statistics_per_model_view(request, model):
    STATISTICS_MODELS_MAP = {
        'merchant': User,
        'widget': Widget,
        'ticket': Ticket,
    }

    objects = (
        STATISTICS_MODELS_MAP[model].objects
        .get_objects_list_by_role(request.user)
    )

    context = {
        'objects': objects,
        'model': model,
    }
    return render(request, 'home/statistics_per_model.html', context)
