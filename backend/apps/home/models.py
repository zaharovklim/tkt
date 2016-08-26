from django.db import models

from apps.tickets.models import Ticket
from apps.utils.models import ModelActionLogMixin


class Widget(ModelActionLogMixin):

    name = models.TextField(
        verbose_name="Name",
    )

    internal_name = models.TextField(
        verbose_name="Internal name",
    )

    enabled = models.BooleanField(
        verbose_name="Is widget enabled",
        default=False,
    )

    tickets = models.ForeignKey(
        Ticket,
        verbose_name="Tickets",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
