# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import uuid
import django.core.validators
import django.utils.timezone
import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', unique=True)),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.IntegerField(null=True)),
                ('signup_method', models.CharField(max_length=10, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('picture', models.ImageField(upload_to='pictures')),
                ('score', models.FloatField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaseClass',
            fields=[
                ('id', django_extensions.db.fields.UUIDField(default=uuid.uuid4, blank=True, editable=False, primary_key=True, serialize=False)),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('uts', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='map_userMovie',
            fields=[
                ('baseclass_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, to='web.BaseClass', auto_created=True)),
            ],
            bases=('web.baseclass',),
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('baseclass_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, to='web.BaseClass', auto_created=True)),
                ('imdbid', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('rtscore', models.FloatField(default=0)),
                ('boscore', models.FloatField(default=0)),
                ('box_office', models.CharField(max_length=100, null=True)),
                ('totalscore', models.FloatField(default=0)),
            ],
            bases=('web.baseclass',),
        ),
        migrations.CreateModel(
            name='otp',
            fields=[
                ('baseclass_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, to='web.BaseClass', auto_created=True)),
                ('code', models.IntegerField(null=True)),
                ('uobj', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('web.baseclass',),
        ),
        migrations.AddField(
            model_name='map_usermovie',
            name='mobj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='web.Movies'),
        ),
        migrations.AddField(
            model_name='map_usermovie',
            name='uobj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='map_usermovie',
            unique_together=set([('uobj', 'mobj')]),
        ),
    ]
