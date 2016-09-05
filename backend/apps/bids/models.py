from django.db import models

from apps.tickets.models import Ticket


class Bid(models.Model):

    BID_STATUSES = (
        ('ACCEPTED', 'accepted'),
        ('PAID', 'paid'),
        ('REJECTED', 'rejected'),
    )

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

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        blank=True
    )

    status = models.CharField(
        verbose_name="Status",
        max_length=8,
        choices=BID_STATUSES,
        default='ACCEPTED',
    )

    def __str__(self):
        return "{} - {} - {}".format(self.ticket, self.bid_price, self.status)
