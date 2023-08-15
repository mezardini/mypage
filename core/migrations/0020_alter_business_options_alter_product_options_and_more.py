# Generated by Django 4.0.4 on 2023-08-05 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_product_reviews_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='product_review',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='business',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
