import os

from django.db import models

import pdfkit
from ckeditor.fields import RichTextField

from conf.settings import (
    MEDIA_ROOT, WKHTMLTOPDF_EXECUTABLE_PATH, ROLES,
)
from apps.utils.models import ModelActionLogMixin
from apps.home.models import Widget


class TicketManager(models.Manager):

    def get_objects_list_by_role(self, user):
        if user.role is ROLES.ADMIN:
            return self.get_queryset()
        elif user.role is ROLES.MERCHANT:
            return self.get_queryset().filter(created_by=user)


class Ticket(ModelActionLogMixin):

    objects = TicketManager()

    widget = models.ForeignKey(
        Widget,
        verbose_name="Widget",
        null=True,
        blank=True,
    )

    name = models.TextField(
        verbose_name="Name",
    )

    internal_name = models.TextField(
        verbose_name="Internal name",
    )

    description = models.TextField(
        verbose_name="Description",
    )

    box_office_price = models.DecimalField(
        verbose_name="Box office price",
        max_digits=6,
        decimal_places=2,
    )

    template = RichTextField(
        verbose_name="Template",
        default="",
    )

    pdf = models.FileField(
        verbose_name="PDF file",
        upload_to=MEDIA_ROOT,
        null=True,
        blank=True,
    )

    min_accepted_bid = models.DecimalField(
        verbose_name="Min accepted bid",
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    max_bid_attempts = models.PositiveSmallIntegerField(
        verbose_name="Amount of times user can bid",
        default=1,
    )

    @property
    def bid_statistics(self):
        bids = self.bid_set.all()
        accepted_count = bids.filter(status="ACCEPTED").count()
        paid_count = bids.filter(status="PAID").count()
        rejected_count = bids.filter(status="REJECTED").count()
        return {
            'accepted': accepted_count,
            'paid': paid_count,
            'rejected': rejected_count,
        }

    def pdf_link(self):
        if self.pdf:
            return '<a href="{}">Download PDF</a>'.format(self.pdf.url)
        else:
            return 'Save the ticket to be able to download PDF'

    pdf_link.short_description = 'PDF file'
    pdf_link.allow_tags = True

    def save(self, *args, **kwargs):
        changed_or_not_exists = False
        if self.pk is None:
            changed_or_not_exists = True
        else:
            orig = Ticket.objects.get(pk=self.pk)
            if orig.template != self.template:
                changed_or_not_exists = True

        super().save(*args, **kwargs)

        if changed_or_not_exists:
            config = pdfkit.configuration(
                wkhtmltopdf=(WKHTMLTOPDF_EXECUTABLE_PATH.encode('utf-8'))
            )
            pdf_file_name = "ticket_{}.pdf".format(self.pk)

            pdfkit.from_string(
                self.template,
                os.path.join(MEDIA_ROOT, pdf_file_name),
                configuration=config,
            )

            self.pdf.name = pdf_file_name
            self.save()

    def __str__(self):
        return self.name
