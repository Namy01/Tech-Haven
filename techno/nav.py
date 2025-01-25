from .models import Product, ProductImage, Category, Addcategory, Advertisement, Tag, Timestamp

def navigations(request):
    tags = Tag.objects.all().order_by("created_at")
    categories_nav = Category.objects.all()[:7]
    procount = Product.objects.all()


    return{
        "tags" : tags,
        "categories_nav" : categories_nav,
        "procount": procount,
    }

    
