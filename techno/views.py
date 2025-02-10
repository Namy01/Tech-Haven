from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from techno.forms import ReviewForm
from django.urls import reverse_lazy
from .models import Advertisement, Cart, CartItem, Product, Review, Tag, Category, WishList
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.db.models import Avg
from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q

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
        context["related_product"] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)

        

        review_data = product.reviews.aggregate(avg_stars=Avg('stars'))
        average_stars = review_data['avg_stars'] if review_data['avg_stars'] is not None else 1
        context["average_stars"] = average_stars

        product.review = int(average_stars) if average_stars is not None else 1
        product.save()
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

class Quickview(DetailView):
    model = Product
    template_name = "tech/pop_ups/quick_view.html"
    context_object_name = "product"





class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_key = request.session.session_key or request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=session_key, is_active=True)

        
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(request.POST.get('quantity', 0))
        cart_item.save()

        return redirect('cart_detail')


class RemoveFromCartView(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return redirect('cart_detail')



class UpdateCartView(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        return redirect('cart_detail')


class UpdateShippingView(View):
    def post(self, request):
        shipping_cost = int(request.POST.get("shipping", 0))
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.shipping_cost = shipping_cost

        coupon_code = int(request.POST.get("coupon_code", 0))
        coupon = 12345

        if coupon_code == coupon:
            cart.discount_cost = 100
        else:
            cart.discount_cost = 0

        cart.save()

        request.session['selected_shipping'] = shipping_cost
        request.session['selected_coupon'] = coupon_code if coupon_code == coupon else None

        total = cart.get_total()
        return JsonResponse({"total": total}) 

class CartDetailView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        selected_shipping = request.session.get('selected_shipping', 0)  # Default to 0

        context = {
            "cart": cart,
            "cart_items": cart.items.all(),
            "subtotal": cart.get_subtotal(),
            "total": cart.get_total(),
            "selected_shipping": selected_shipping,
        }
        return render(request, "tech/cart/cart.html", context)
    
class WishListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist_items = WishList.objects.filter(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            wishlist_items = WishList.objects.filter(session_key=request.session.session_key)

        return render(request, 'tech/cart/wishlist.html', {'wishlist_items': wishlist_items})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            wishlist_item, created = WishList.objects.get_or_create(session_key=request.session.session_key, product=product)

        if not created:
            wishlist_item.delete()

        return redirect('wishlist')

    
class ProductSearchView(View):
    template_name = "tech/list/list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET["query"]
        products = Product.objects.filter(
            (Q(name__icontains=query)))

        

        return render(
            request,
            self.template_name,
            {"products":products, "query": query},
        )
    




     



    

    
