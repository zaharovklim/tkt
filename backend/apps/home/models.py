import barcode, os
from barcode.writer import ImageWriter

from django.db import models
from django.contrib.auth.models import User, Group

from import_export import resources
from image_cropping import ImageRatioField

from conf.settings import ADMIN_GROUP_NAME, MERCHANT_GROUP_NAME
from apps.utils.models import ModelActionLogMixin
from conf.settings import MERCHANT_GROUP_NAME, BARCODE_PATH


# ----------------------------------------------------------------------------
# Extending of User model
# ----------------------------------------------------------------------------

def get_role(self):
    groups = self.groups.all()

    merchant = Group.objects.get(name=MERCHANT_GROUP_NAME)
    admin = Group.objects.get(name=ADMIN_GROUP_NAME)

    if merchant in groups:
        return MERCHANT_GROUP_NAME
    elif admin in groups:
        return ADMIN_GROUP_NAME
    else:
        raise ValueError(
            'User has no appropriate group, there only "Merchant" and "Admin" '
            'groups supported by system'
        )

User.add_to_class('get_role', get_role)


def bid_statistics(self):
    widgets = self.widget_set.all()
    statistics = {'accepted': 0, 'paid': 0, 'rejected': 0}
    for widget in widgets:
        for property in widget.bid_statistics.keys():
            statistics[property] += widget.bid_statistics[property]
    return statistics

User.add_to_class('bid_statistics', bid_statistics)


class UserManager(models.Manager):

    def get_objects_list_by_role(self, user):
        role = user.get_role()

        if role == ADMIN_GROUP_NAME:
            return self.get_queryset()
        elif role == MERCHANT_GROUP_NAME:
            return (user, )

User.add_to_class('objects', UserManager())

# ----------------------------------------------------------------------------


class WidgetManager(models.Manager):

    def get_objects_list_by_role(self, user):
        role = user.get_role()
        if role == ADMIN_GROUP_NAME:
            return self.get_queryset()
        elif role == MERCHANT_GROUP_NAME:
            return self.get_queryset().filter(created_by=user)


class Widget(ModelActionLogMixin):

    objects = WidgetManager()

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

    @property
    def bid_statistics(self):
        tickets = self.ticket_set.all()
        statistics = {'accepted': 0, 'paid': 0, 'rejected': 0}
        for ticket in tickets:
            print(ticket.bid_statistics)
            print(ticket.name)
            print(ticket.id)
            print()
            for property in ticket.bid_statistics.keys():

                statistics[property] += ticket.bid_statistics[property]

        return statistics

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
        null=True,
        blank=True
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
	    verbose_name='Barcode format',
        choices=FORMAT_CHOISES,
	    default=EAN13,
	    max_length=21
    )

    image = models.ImageField(
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.merchant)

    def save(self):
        if not os.path.exists(BARCODE_PATH):
            os.makedirs(BARCODE_PATH)
        get_barcode = barcode.get_barcode_class(self.format)
        image = get_barcode(str(self.barcode), writer=ImageWriter())
        self.image = image.save(os.path.join(BARCODE_PATH, str(self.barcode)))
        super().save()
