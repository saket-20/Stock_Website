# Generated by Django 3.1.7 on 2021-04-13 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0010_auto_20210412_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='stock1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_app.stocks'),
        ),
    ]