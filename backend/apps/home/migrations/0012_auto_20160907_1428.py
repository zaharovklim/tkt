# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-07 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_barcodeimage_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Planned', 'Planned'), ('Published', 'Published'), ('Unpublished', 'Unpublished')], default='Draft', max_length=11, verbose_name='Widget status'),
        ),
        migrations.AddField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('Regular', 'Regular'), ('Dynamic', 'Dynamic')], default='Dynamic', max_length=7, verbose_name='Widget type'),
        ),
        migrations.AlterField(
            model_name='barcodeimage',
            name='format',
            field=models.CharField(choices=[('ean13', 'EAN-8'), ('ean8', 'EAN-13'), ('code128', 'Code-128'), ('code39', 'Starndard-39')], default='ean13', max_length=21, verbose_name='Barcode format'),
        ),
        migrations.AlterField(
            model_name='barcodeimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]