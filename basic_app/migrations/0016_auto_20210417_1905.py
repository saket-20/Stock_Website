# Generated by Django 3.1.7 on 2021-04-17 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0015_userprofileinfo_shares_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='no_of_trades_today',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='shares_count',
            field=models.PositiveIntegerField(default=50),
        ),
    ]
