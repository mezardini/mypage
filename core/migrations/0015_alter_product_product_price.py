# Generated by Django 4.0.4 on 2023-08-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_business_business_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(null=True),
        ),
    ]