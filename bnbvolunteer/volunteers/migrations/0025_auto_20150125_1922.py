# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0024_auto_20150124_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='code',
            field=models.CharField(unique=True, max_length=20),
            preserve_default=True,
        ),
    ]
