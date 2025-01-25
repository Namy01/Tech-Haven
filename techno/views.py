from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from techno.forms import ReviewForm
from django.urls import reverse_lazy
from .models import Advertisement, Product, Review, Tag, Category
from django.views.generic import ListView, DetailView, TemplateView, CreateView

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

class ProductListView(ListView):
    model = Product
    template_name = "tech/list/list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.exclude(pk__in=[5, 8, 6, 7]).order_by("-created_at")[:10]


class Productbycategory(ListView):
    model = Product
    template_name = "tech/list/list.html"
    context_object_name = "products"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.exclude(pk__in=[5, 8, 6, 7]).filter(
             category__id = self.kwargs["category_id"],
        ).order_by("-created_at")
        return query
    

class Productbytag(ListView):
    model = Product
    template_name = "tech/list/list.html"
    context_object_name = "products"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.exclude(pk__in=[5, 8, 6, 7]).filter(
             tags__id = self.kwargs["tag_id"],
        ).order_by("-created_at")
        return query
    
class ProductDetail(DetailView):
    model = Product
    template_name = "tech/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["reviews"] = Review.objects.filter( product=product)
        return context

class ReviewView(View):
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST, request.FILES)
        product_id = request.POST.get("product")
        
        if not product_id:
            messages.error(request, "Product not found.")
            return redirect("some_fallback_url")
        
        product = get_object_or_404(Product, pk=product_id)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect("product-detail", pk=product_id)

        
        return render(
            request,
            "tech/product_detail.html",
            {"product": product, "form": form}
        )
    
