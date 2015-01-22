# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0021_auto_20150120_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='generateDate',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
