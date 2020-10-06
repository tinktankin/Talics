# Generated by Django 3.1 on 2020-09-23 13:22

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MappingFor', models.TextField(null=True)),
                ('CreatedOn', models.DateField(auto_now_add=True, null=True)),
                ('Mappings', django.contrib.postgres.fields.hstore.HStoreField(null=True)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='user.user')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
