# Generated by Django 3.1 on 2020-09-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AgencyName', models.TextField(null=True)),
                ('Location', models.TextField(null=True)),
                ('Website', models.TextField(null=True)),
                ('ContractStartedOn', models.DateField(null=True)),
                ('ContractValidTill', models.DateField(null=True)),
                ('KCName', models.TextField(null=True)),
                ('KCEmail', models.EmailField(max_length=254, null=True)),
                ('KCPhone', models.IntegerField(null=True)),
            ],
        ),
    ]
