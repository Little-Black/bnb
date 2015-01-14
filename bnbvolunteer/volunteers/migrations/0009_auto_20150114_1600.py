# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0008_auto_20150113_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='redemptionActivity',
            field=models.ForeignKey(to='volunteers.Activity', null=True),
            preserve_default=True,
        ),
    ]
