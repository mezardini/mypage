# Generated by Django 4.0.4 on 2023-07-16 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.TextField(unique=True)),
                ('business_email', models.EmailField(max_length=254)),
                ('business_location', models.CharField(blank=True, max_length=500, null=True)),
                ('business_contact_number', models.CharField(blank=True, max_length=500, null=True)),
                ('business_instagram_link', models.URLField(blank=True, null=True)),
                ('business_facebook_link', models.URLField(blank=True, null=True)),
                ('business_twitter_link', models.URLField(blank=True, null=True)),
                ('business_linkedin_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestimonialSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testimony_name', models.TextField()),
                ('testimony_description', models.TextField()),
                ('role_of_testifier', models.TextField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_title', models.TextField()),
                ('service_description', models.TextField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
            ],
        ),
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_headline', models.TextField()),
                ('hero_usp', models.TextField(blank=True, null=True)),
                ('hero_image', models.ImageField(upload_to='media')),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
            ],
        ),
        migrations.CreateModel(
            name='AboutUsSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_us_headline', models.TextField(blank=True, null=True)),
                ('about_us_description', models.TextField(blank=True, null=True)),
                ('about_us_image', models.TextField(blank=True, null=True)),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.business')),
            ],
        ),
    ]
