# Generated by Django 3.0.8 on 2020-08-04 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20200803_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerageService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
