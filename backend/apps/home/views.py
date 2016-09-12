from django.shortcuts import render
from django.http import HttpResponseBadRequest

from apps.tickets.models import Article
from apps.bids.models import Bid


def index(request):
    context = {}

    if not request.session.exists(request.session.session_key):
        request.session.create()

    if request.method == 'POST':
        # --------------------------------------------------------------------
        # Get and clean ticket_id, bid_price and number_of_tickets
        try:
            ticket_id = int(request.POST.get('ticket_id'))
        except ValueError:
            return HttpResponseBadRequest("Ticket id is invalid")

        try:
            bid_price = float(request.POST.get('bid_price'))
        except ValueError:
            return HttpResponseBadRequest("Bid price is invalid")

        try:
            number_of_tickets = int(request.POST.get('number_of_tickets'))
        except ValueError:
            return HttpResponseBadRequest("Number of tickets is invalid")

        # --------------------------------------------------------------------
        # Increment bid_attempts counter
        if request.session.get('bid_attempts') is None:
            request.session['bid_attempts'] = 1
        else:
            request.session['bid_attempts'] += 1
        bid_attempts = request.session['bid_attempts']

        # --------------------------------------------------------------------
        # Select and test for existence of Ticket user trying to bid
        try:
            ticket = Article.objects.get(id=ticket_id)
        except Article.DoesNotExist:
            return HttpResponseBadRequest("Ticket does not exist")

        # --------------------------------------------------------------------
        # Validate Ticket's bid restriction for maximum attempts
        if bid_attempts > ticket.max_bid_attempts:
            return HttpResponseBadRequest(
                "Bid attempts have exceeded maximum for this ticket"
            )

        # --------------------------------------------------------------------
        bid_status = Bid.REJECTED
        response = "You lose"
        if bid_price > ticket.min_accepted_bid:
            bid_status = Bid.ACCEPTED
            response = "You won"

        # TODO: offer to user fill the order form
        context['reponse'] = response

        Bid.objects.create(
            session_key=request.session.session_key,
            ticket=ticket,
            bid_price=bid_price,
            number_of_tickets=number_of_tickets,
            status=bid_status,
        )

    return render(request, 'home/index.html', context)
