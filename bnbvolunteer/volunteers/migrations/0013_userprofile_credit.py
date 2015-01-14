# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0012_auto_20150114_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='credit',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
