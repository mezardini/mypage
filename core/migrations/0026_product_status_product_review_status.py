# Generated by Django 4.0.4 on 2023-08-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Hidden', 'Hidden'), ('Active', 'Active')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product_review',
            name='status',
            field=models.CharField(choices=[('Hidden', 'Hidden'), ('Active', 'Active')], max_length=10, null=True),
        ),
    ]
