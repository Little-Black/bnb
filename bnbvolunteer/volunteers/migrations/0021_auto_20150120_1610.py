# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0020_auto_20150116_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationrequest',
            name='creationTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 21, 10, 44, 1419, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
