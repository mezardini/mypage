# Generated by Django 4.0.4 on 2023-08-05 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(default='', upload_to='media'),
        ),
    ]
