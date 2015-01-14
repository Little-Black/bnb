# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0007_auto_20150112_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='code',
            field=models.CharField(default=b'\x03\x15\x13\x19\x08\x00\x16\x16\x11\x01\x02\x19\x13\x17\x08\x08\x05\x0c\x18\r', max_length=20),
            preserve_default=True,
        ),
    ]
