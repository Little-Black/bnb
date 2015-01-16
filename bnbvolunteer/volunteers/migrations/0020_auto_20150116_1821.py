# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0019_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='dateDone',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
