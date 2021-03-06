# Generated by Django 4.0.3 on 2022-04-05 06:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=192)),
                ('starting_bid_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_url', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='auction_category', to='auctions.auctioncategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_listing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
