from django.contrib import admin
from .models import Product, Category, Wishlist, Cart, OrderItem, Order, ProductImage, Color

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ProductImage)
admin.site.register(Color)


# Register your models here.
