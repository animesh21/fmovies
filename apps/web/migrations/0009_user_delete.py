# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_movies_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='delete',
            field=models.BooleanField(default=False),
        ),
    ]
