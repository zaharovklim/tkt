from django.db import models
from import_export import resources

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


class Barcode(models.Model):

    article = models.IntegerField(
        verbose_name="Article",
        null=True,
        blank=True
    )

    barcode = models.BigIntegerField(
        verbose_name="Barcode",
        null = True,
        blank = True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.barcode

    def __str__(self):
        barcode = str(self.barcode)
        return barcode


class BarcodeResource(resources.ModelResource):
    class Meta:
        model = Barcode
