# Generated by Django 4.0.1 on 2022-03-09 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidhur2shop', '0002_cart_product_order_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='name',
            field=models.CharField(default='name', max_length=200),
        ),
    ]