# Generated by Django 5.0 on 2023-12-12 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener_app', '0003_urlmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmodel',
            name='short_url',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
