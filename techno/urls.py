
from django.urls import path
from techno import views

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("list-view", views.ProductListView.as_view(), name= "list-view"),
    path("Product-by-category/<int:category_id>/", views.Productbycategory.as_view(), name= "Product-by-category"),
    path("Product-by-tag/<int:tag_id>/", views.Productbytag.as_view(), name= "Product-by-tag"),
    path("product-detail/<int:pk>/", views.ProductDetail.as_view(), name= "product-detail"),
    path('product/<int:pk>/review/', views.ReviewView.as_view(), name='add_review'),
    path('quick-view/<int:pk>/', views.Quickview.as_view(), name='quick-view'),
    path("cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart-add/<int:product_id>/",  views.AddToCartView.as_view(), name="cart-add"),
    path('cart-update/<int:cart_item_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path("cart-remove/<int:cart_item_id>/",  views.RemoveFromCartView.as_view(), name="cart-remove"),
    path("update-shipping/", views.UpdateShippingView.as_view(), name="update_shipping"),
    
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>/', views.WishListView.as_view(), name='wishlist-add-remove'),

]
