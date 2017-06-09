# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20170215_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('baseclass_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, primary_key=True, to='web.BaseClass')),
                ('group_name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('group_admin', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='admin', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            bases=('web.baseclass',),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('baseclass_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, primary_key=True, to='web.BaseClass')),
                ('userActive', models.BooleanField(default=True)),
                ('group', models.ForeignKey(to='web.Group', verbose_name='group', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('uobj', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            bases=('web.baseclass',),
        ),
        migrations.AlterUniqueTogether(
            name='usergroup',
            unique_together=set([('uobj', 'group')]),
        ),
    ]
