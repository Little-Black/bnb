# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0017_auto_20150116_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activityType',
            field=models.ForeignKey(default=b'', to='volunteers.ActivityType', null=True),
            preserve_default=True,
        ),
    ]
