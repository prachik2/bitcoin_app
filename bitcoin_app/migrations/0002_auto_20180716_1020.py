# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-16 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GenerateBitcoinAddress',
            new_name='GenerateAddress',
        ),
    ]