# Generated by Django 5.0 on 2023-12-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlmodel',
            name='use_amount',
            field=models.IntegerField(default=0),
        ),
    ]
