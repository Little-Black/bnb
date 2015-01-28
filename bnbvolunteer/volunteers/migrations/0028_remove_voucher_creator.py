# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0027_voucher_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher',
            name='creator',
        ),
    ]
