# Generated by Django 3.1.7 on 2021-04-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0005_auto_20170307_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='stocks',
            fields=[
                ('symbol', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('prevclose', models.IntegerField()),
                ('open', models.IntegerField()),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
                ('Last', models.IntegerField()),
            ],
        ),
    ]
