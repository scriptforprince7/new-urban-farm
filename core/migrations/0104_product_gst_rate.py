# Generated by Django 4.2.4 on 2024-03-22 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0103_remove_cartorder_razor_pay_order_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="gst_rate",
            field=models.CharField(default="18%", max_length=100),
        ),
    ]
