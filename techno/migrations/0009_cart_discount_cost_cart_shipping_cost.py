# Generated by Django 5.1.5 on 2025-01-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techno', '0008_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='shipping_cost',
            field=models.IntegerField(default=0),
        ),
    ]
