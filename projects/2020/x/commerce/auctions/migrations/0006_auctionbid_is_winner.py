# Generated by Django 4.0.3 on 2022-04-10 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionbid',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]
