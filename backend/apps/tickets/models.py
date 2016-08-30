import os

from django.db import models

import pdfkit
from ckeditor.fields import RichTextField

from conf.settings import MEDIA_ROOT, WKHTMLTOPDF_EXECUTABLE_PATH
from apps.utils.models import ModelActionLogMixin
from apps.home.models import Widget


class Ticket(ModelActionLogMixin):

    widget = models.ForeignKey(
        Widget,
        verbose_name="Widget",
        null=True,
        blank=True,
    )

    name = models.TextField(
        verbose_name="Name",
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
        verbose_name="Box office price",
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    max_bid_attempts = models.PositiveSmallIntegerField(
        verbose_name="Amount of times user can bid",
        default=1,
    )

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
