# Generated by Django 4.2.4 on 2024-08-09 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0131_remove_productreview_product_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="deal_of_week",),
        migrations.RemoveField(model_name="product", name="featured",),
    ]
