# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 22:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_auto_20170517_1159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-timestamp']},
        ),
    ]
