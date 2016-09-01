from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from apps.tickets.models import Ticket
from apps.bids.models import Bid
from apps.home.models import Widget


STATISTICS_MODELS = {
    'user': User,
    'widget': Widget,
    'ticket': Ticket,
}


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


def bid_statistics(request):
    context = {
        'statistics_data':
            [
                {"label": "accepted", "value": 540},
                {"label": "paid", "value": 120},
                {"label": "rejected", "value": 200}
            ]
    }
    return render(request, 'home/statistics.html', context)


# TODO: restrict access to staff
def bid_statistics_list_per_model(request, model):

    objects = (
        STATISTICS_MODELS[model].objects.get_objects_list_by_role(request.user)
    )

    context = {'objects': objects}

    return render(request, 'home/statistics_per_model.html', context)
