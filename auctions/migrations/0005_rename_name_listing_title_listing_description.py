# Generated by Django 5.2.3 on 2025-07-02 21:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_listing_starting_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="name",
            new_name="title",
        ),
        migrations.AddField(
            model_name="listing",
            name="description",
            field=models.CharField(default="Nimbus 5000 broomstick", max_length=512),
            preserve_default=False,
        ),
    ]
