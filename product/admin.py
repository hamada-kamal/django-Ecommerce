from .models import Product, Customer, Order, OrderItem, ShippingAddress
from django.contrib import admin
 


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)