# Generated by Django 5.1 on 2024-08-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_reviewrating_options_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_type',
            field=models.CharField(blank=True, choices=[('amount', 'Amount'), ('percent', 'Percentage')], max_length=10, null=True),
        ),
    ]
