from .models import Product, ProductImage, Category, Addcategory, Advertisement, Tag, Timestamp

def navigations(request):
    tags = Tag.objects.all().order_by("created_at")
    categories_nav = Category.objects.all()[:7]
<<<<<<< HEAD
    procount = Product.objects.all()
=======
>>>>>>> 23ae40177c1685d026168855d97ac3cd74c5db18

    return{
        "tags" : tags,
        "categories_nav" : categories_nav,
<<<<<<< HEAD
        "procount": procount,
=======
        
>>>>>>> 23ae40177c1685d026168855d97ac3cd74c5db18
        }
    
