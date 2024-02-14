# Generated by Django 5.0 on 2024-01-28 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon_banner', '0003_usercoupon_is_applyed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercoupon',
            name='is_used',
        ),
        migrations.AddField(
            model_name='usercoupon',
            name='reduced_price',
            field=models.FloatField(default=0),
        ),
    ]