from django.db import models

from apps.tickets.models import Ticket


class Bid(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        verbose_name="Ticket",
    )

    session_key = models.CharField(
        verbose_name="Session key",
        max_length=32
    )

    bid_price = models.DecimalField(
        verbose_name="Bid price",
        max_digits=6,
        decimal_places=2,
    )

    # TODO: creation time

    def __str__(self):
        return "{} - {}".format(self.ticket, self.bid_price)
