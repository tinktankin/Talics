# Generated by Django 3.1 on 2020-08-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20200830_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='staging',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
