from django.shortcuts import render
from .models import Advertisement, Product, Tag, Category
from django.views.generic import ListView, DetailView

class HomeView(ListView):
    model = Product
    template_name = "tech/home.html"
    context_object_name = "products"
    queryset = Product.objects.all()[4:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all().order_by("created_at")[2:10]
        context["tags"] = Tag.objects.all().order_by("created_at")
        context["recommended"] = Product.objects.exclude(pk__in=[5, 8, 6, 7]).order_by("-created_at")[:10]
        context["add1"] = Advertisement.objects.all()[:3]


        
        return context


