# Generated by Django 4.2.4 on 2024-08-09 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0134_productvarianttypes_in_stock"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartorder",
            old_name="billingaddress",
            new_name="billing_address_line1",
        ),
        migrations.RenameField(
            model_name="cartorder",
            old_name="shippingaddress",
            new_name="billing_address_line2",
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_checkout_city",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_checkout_district",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_checkout_division",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_checkout_state",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_street_address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="billing_zipcode",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="shipping_address_line1",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="shipping_address_line2",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="shipping_street_address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
