# Generated by Django 4.0.4 on 2023-07-19 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_servicesection_business_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.TextField(null=True)),
                ('product_description', models.TextField(null=True)),
                ('product_price', models.TextField(null=True)),
                ('product_payment_link', models.URLField(null=True)),
                ('slug', models.TextField(null=True, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(null=True, upload_to='media')),
                ('video', models.ImageField(null=True, upload_to='media')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='aboutussection',
            name='business',
        ),
        migrations.RemoveField(
            model_name='herosection',
            name='business',
        ),
        migrations.DeleteModel(
            name='ServiceSection',
        ),
        migrations.RemoveField(
            model_name='testimonialsection',
            name='business',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_call_to_action',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_cta_name',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_facebook_link',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_instagram_link',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_linkedin_link',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_location',
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_twitter_link',
        ),
        migrations.AddField(
            model_name='business',
            name='slug',
            field=models.TextField(null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='AboutUsSection',
        ),
        migrations.DeleteModel(
            name='HeroSection',
        ),
        migrations.DeleteModel(
            name='TestimonialSection',
        ),
        migrations.AddField(
            model_name='product',
            name='business',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.business'),
        ),
    ]
