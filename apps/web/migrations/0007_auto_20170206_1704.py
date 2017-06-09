# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_upcoming_movies'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upcoming_movies',
            old_name='name',
            new_name='title',
        ),
    ]
