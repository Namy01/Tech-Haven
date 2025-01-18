from django.contrib import admin
from techno.models import Category, Product, ProductImage, Tag

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductImage)