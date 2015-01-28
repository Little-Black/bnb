# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0025_auto_20150125_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='generateDate',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
