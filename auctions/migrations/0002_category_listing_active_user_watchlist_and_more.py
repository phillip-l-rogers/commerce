# Generated by Django 5.2.3 on 2025-07-02 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("picture", models.ImageField(upload_to="")),
                ("created", models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name="listing",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="user",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True, related_name="watchers", to="auctions.listing"
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="picture",
            field=models.ImageField(blank=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="listing",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="listings",
                to="auctions.category",
            ),
        ),
    ]
