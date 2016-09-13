# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-13 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0007_auto_20160908_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('firstname', models.CharField(blank=True, max_length=255, null=True, verbose_name='First name')),
                ('lastname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
            ],
        ),
    ]
