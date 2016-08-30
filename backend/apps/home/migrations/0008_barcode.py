# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-30 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_widget_tickets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.IntegerField(blank=True, null=True, verbose_name='Article')),
                ('barcode', models.BigIntegerField(blank=True, null=True, verbose_name='Barcode')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]