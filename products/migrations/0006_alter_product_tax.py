# Generated by Django 5.1 on 2024-08-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_shipping_fee_product_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tax',
            field=models.PositiveIntegerField(blank=True, help_text='tax in pecentage', null=True),
        ),
    ]
