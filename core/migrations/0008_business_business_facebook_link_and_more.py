# Generated by Django 4.0.4 on 2023-07-22 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_product_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='business_facebook_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='business_instagram_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='business_linkedin_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='business_secret_key',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='business_twitter_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
