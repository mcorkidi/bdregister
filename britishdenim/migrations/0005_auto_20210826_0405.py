# Generated by Django 3.2.5 on 2021-08-26 04:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('britishdenim', '0004_auto_20210826_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 26, 4, 5, 24, 303663, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='image',
            field=models.ImageField(default='coupon.jpg', upload_to='britishdenim/static/britishdenim/coupon_images'),
        ),
    ]
