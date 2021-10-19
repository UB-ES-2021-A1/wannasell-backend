from django.contrib import admin

# Register your models here.
from products.models import Category, Product, Image

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
