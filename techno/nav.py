from django.shortcuts import render
from .models import Product, ProductImage, Category, Addcategory, Advertisement, Tag, Timestamp, CartItem, Cart, WishList

def navigations(request):
    tags = Tag.objects.all().order_by("created_at")
    categories_nav = Category.objects.all()[:7]
    procount = Product.objects.all()
    cart_item_count = CartItem.objects.all()
    WishList_item_count = WishList.objects.all()
   

    
    
    
    
    return{
        "tags" : tags,
        "categories_nav" : categories_nav,
        "procount": procount,
        "cart_item_count": cart_item_count,
        "WishList_item_count": cart_item_count,
       
        
    }

def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = WishList.objects.filter(user=request.user, is_active=True)
    else:
        wishlist_items = WishList.objects.filter(session_key=request.session.session_key, is_active=True)

    
    is_in_wishlist = [item.product.id for item in wishlist_items]

    return{
        
        "wishlist_items": wishlist_items,
        "is_in_wishlist": is_in_wishlist,
    }

    
