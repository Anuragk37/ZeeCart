# Generated by Django 5.0 on 2024-01-28 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon_banner', '0004_remove_usercoupon_is_used_usercoupon_reduced_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercoupon',
            name='reduced_price',
            field=models.FloatField(),
        ),
    ]
