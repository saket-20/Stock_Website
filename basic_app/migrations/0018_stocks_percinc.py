# Generated by Django 3.1.7 on 2021-04-19 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0017_auto_20210419_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='percinc',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
    ]
