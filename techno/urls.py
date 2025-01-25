
from django.urls import path
from techno import views

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("list-view", views.ProductListView.as_view(), name= "list-view"),
    path("Product-by-category/<int:category_id>/", views.Productbycategory.as_view(), name= "Product-by-category"),
    path("Product-by-tag/<int:tag_id>/", views.Productbytag.as_view(), name= "Product-by-tag"),
    path("product-detail/<int:pk>/", views.ProductDetail.as_view(), name= "product-detail"),
    path('product/<int:pk>/review/', views.ReviewView.as_view(), name='add_review'),

]
