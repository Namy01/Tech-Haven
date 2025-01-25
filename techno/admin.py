from django.contrib import admin
from techno.models import Addcategory, Advertisement, Category, Product, ProductImage, Review, Tag
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductImage)
admin.site.register(Addcategory)
admin.site.register(Advertisement)
admin.site.register(Review)





class SomeModelAdmin(SummernoteModelAdmin):  
    summernote_fields = '__all__'

admin.site.register(Product, SomeModelAdmin)