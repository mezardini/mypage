# Generated by Django 4.0.4 on 2023-07-30 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_product_media_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='business_email',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_secret_key',
        ),
        migrations.AddField(
            model_name='business',
            name='business_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product_media',
            name='video',
            field=models.FileField(blank=True, default='/static/images/nva.mov', null=True, upload_to='media'),
        ),
    ]
