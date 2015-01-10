# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0003_userlog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='date',
            field=models.CharField(max_length=200),
        ),
    ]
