# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='dateDone',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='dateEntered',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='voucher',
            name='redemptionActivity',
            field=models.ForeignKey(blank=True, to='volunteers.Activity', null=True),
            preserve_default=True,
        ),
    ]
