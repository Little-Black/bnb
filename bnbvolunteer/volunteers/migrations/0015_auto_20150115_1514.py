# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='dateDone',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
