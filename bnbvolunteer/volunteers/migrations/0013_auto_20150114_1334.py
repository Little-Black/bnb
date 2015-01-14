# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0012_auto_20150114_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='dateEntered',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
