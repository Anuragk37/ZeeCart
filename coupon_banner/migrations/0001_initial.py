# Generated by Django 5.0 on 2024-01-14 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='')),
                ('banner_image', models.ImageField(upload_to='banner_image')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('link', models.CharField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('discount', models.FloatField()),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('min_order', models.FloatField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsedCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_used', models.BooleanField(default=False)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupon_banner.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]