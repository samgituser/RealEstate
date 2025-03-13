# Generated by Django 5.1.7 on 2025-03-12 09:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('property_type', models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('commercial', 'Commercial'), ('land', 'Land')], max_length=20)),
                ('listing_type', models.CharField(choices=[('sale', 'For Sale'), ('rent', 'For Rent')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('bedrooms', models.PositiveIntegerField(blank=True, null=True)),
                ('bathrooms', models.PositiveIntegerField(blank=True, null=True)),
                ('square_feet', models.PositiveIntegerField(blank=True, null=True)),
                ('year_built', models.PositiveIntegerField(blank=True, null=True)),
                ('has_pool', models.BooleanField(default=False)),
                ('has_gym', models.BooleanField(default=False)),
                ('has_parking', models.BooleanField(default=False)),
                ('has_elevator', models.BooleanField(default=False)),
                ('has_security', models.BooleanField(default=False)),
                ('is_furnished', models.BooleanField(default=False)),
                ('has_air_conditioning', models.BooleanField(default=False)),
                ('has_heating', models.BooleanField(default=False)),
                ('main_image', models.ImageField(upload_to='properties/main/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='properties/gallery/')),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='properties.property')),
            ],
        ),
    ]
