# Generated by Django 5.0 on 2024-01-20 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_order', '0006_alter_orderitems_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='return_status',
            field=models.CharField(blank=True, choices=[('Request', 'Request'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=50, null=True),
        ),
    ]