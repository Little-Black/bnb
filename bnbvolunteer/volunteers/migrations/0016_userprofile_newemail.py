# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0015_auto_20150115_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='newEmail',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
    ]
