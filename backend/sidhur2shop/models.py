#from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class APIUser(AbstractUser):
    pass

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=500, null = False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    product_image = models.FileField(upload_to='products')
    MOBILE = 'Mob'
    COMPUTER = 'Com'
    TV = 'Tv'
    CONSOLE = 'Con'
    TABLET = 'Tab'
    TAGS = [
        (MOBILE, 'Mobile'),
        (COMPUTER, 'Computer'),
        (TV, 'Tv'),
        (CONSOLE, 'Console'),
        (TABLET, 'Tablet'),
    ]
    tags = models.CharField(
        max_length=20,
        choices=TAGS,
        default=MOBILE,
    )

class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)

class BasketItems(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def item_price(self):
	    return self.product_id.price * self.quantity

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    address = models.CharField(max_length=100, null=False)
    instructions = models.CharField(max_length=200, null=False)
    FAILED = 'FL'
    PROCESSING = 'PR'
    COMPLETED = 'CP'
    STOCKED = 'SC'
    DISPATCHED = 'DP'
    SHIPPED = 'SH'
    ARRIVED = 'AR'
    ORDER_STATUS = [
        (FAILED, 'Failed'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
    ]
    PAYMENT_STATUS = [
        (STOCKED, 'Stocked'),
        (DISPATCHED, 'Dispatched'),
        (ARRIVED, 'Arrived'),
        (SHIPPED, 'Shipped'),
    ]
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default=PROCESSING,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default=STOCKED,
    )

