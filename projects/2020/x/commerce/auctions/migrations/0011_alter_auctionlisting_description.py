# Generated by Django 4.0.3 on 2022-04-12 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auctionlisting_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(max_length=640),
        ),
    ]
