# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_user_delete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='map_usermovie',
            options={'verbose_name': 'User Selected Movies', 'verbose_name_plural': 'User Selected Movies'},
        ),
        migrations.AlterModelOptions(
            name='movies',
            options={'verbose_name': 'Movies', 'verbose_name_plural': 'Movies'},
        ),
        migrations.AlterModelOptions(
            name='upcoming_movies',
            options={'verbose_name': 'Admin Added Movies', 'verbose_name_plural': 'Admin Added Movies'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Fantasy Users', 'verbose_name_plural': 'Fantasy Users'},
        ),
        migrations.AlterField(
            model_name='map_usermovie',
            name='mobj',
            field=models.ForeignKey(verbose_name='movie', on_delete=django.db.models.deletion.DO_NOTHING, to='web.Movies'),
        ),
        migrations.AlterField(
            model_name='map_usermovie',
            name='uobj',
            field=models.ForeignKey(verbose_name='user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(null=True, max_length=12),
        ),
        migrations.AlterUniqueTogether(
            name='map_usermovie',
            unique_together=set([]),
        ),
    ]
