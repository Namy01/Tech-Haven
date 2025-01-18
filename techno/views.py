from django.shortcuts import render
from .models import Product, Tag, Category
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    model = Product
    template_name = "tech/home.html"
    context_object_name = "products"
    queryset = Product.objects.all().order_by("-updated_at")[:3]

