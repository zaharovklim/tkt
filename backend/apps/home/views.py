from django.shortcuts import render
from django.http import HttpResponseBadRequest

from apps.tickets.models import Ticket
from apps.bids.models import Bid


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
