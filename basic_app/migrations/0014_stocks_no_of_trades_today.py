# Generated by Django 3.1.7 on 2021-04-16 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0013_auto_20210414_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='no_of_trades_today',
            field=models.IntegerField(default=50),
        ),
    ]
