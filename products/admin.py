from django.contrib import admin
from .models import Product,ProductCategory, WishlistItem

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(WishlistItem)