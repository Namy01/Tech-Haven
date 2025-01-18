from django.shortcuts import render
from .models import Product, Tag, Category
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    model = Product
    template_name = "tech/home.html"
    context_object_name = "products"
    queryset = Product.objects.all()[4:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("created_at")[2:10]

        return context


