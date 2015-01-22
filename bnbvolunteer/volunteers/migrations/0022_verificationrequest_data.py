# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0021_auto_20150120_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='data',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
