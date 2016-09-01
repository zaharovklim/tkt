# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-31 13:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_ticketimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarcodeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('barcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Barcode')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]