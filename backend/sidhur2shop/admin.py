from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(APIUser)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Order)