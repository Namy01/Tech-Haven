# Generated by Django 5.1.5 on 2025-01-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techno', '0005_alter_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
