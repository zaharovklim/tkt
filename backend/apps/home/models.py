import barcode, os
from barcode.writer import ImageWriter

from django.db import models
from django.contrib.auth.models import User

from import_export import resources
from image_cropping import ImageRatioField

from apps.utils.models import ModelActionLogMixin
from conf.settings import MEDIA_URL, MERCHANT_GROUP_NAME


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

    def __str__(self):
        return str(self.barcode)


class BarcodeResource(resources.ModelResource):
    class Meta:
        model = Barcode

class TicketImage(models.Model):

    merchant = models.ForeignKey(
        User, limit_choices_to={'groups__name': MERCHANT_GROUP_NAME}
    )

    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True
    )

    cropped_img = ImageRatioField('image', '360x360')

    def __str__(self):
        return str(self.merchant)


class BarcodeImage(models.Model):

    EAN13 = 'ean13'
    EAN8 = 'ean8'
    CODE128 = 'code128'
    STANDARD39 = 'code39'
    FORMAT_CHOISES = (
        (EAN13, 'EAN-8'),
        (EAN8, 'EAN-13'),
        (CODE128, 'Code-128'),
        (STANDARD39, 'Starndard-39'),
    )

    merchant = models.ForeignKey(
        User, limit_choices_to={'groups__name': MERCHANT_GROUP_NAME}
    )

    barcode = models.ForeignKey(
        Barcode
    )

    format = models.CharField(
        choices=FORMAT_CHOISES, default=EAN13, max_length=21,
        verbose_name='Barcode format'
    )

    image = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.merchant)

    def save(self):
        save_dir = MEDIA_URL + 'barcodes/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        get_barcode = barcode.get_barcode_class(str(self.format))
        image = get_barcode(str(self.barcode), writer=ImageWriter())
        self.image = image.save(save_dir + str(self.barcode))
        super().save()
