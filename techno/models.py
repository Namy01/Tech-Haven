from django.db import models

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(Timestamp):
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='category/image/' , default="")

    def __str__(self):
        return self.name
    
class Addcategory(Timestamp):
    name = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.name

    
class Tag(Timestamp):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.alt_text or f"Image {self.id}"
        
class Product(Timestamp):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    short_description = models.TextField(default="")
    additional_info = models.TextField(default="")
    review = models.PositiveSmallIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    main_image = models.ImageField(upload_to='products/main_images/')
    gallery_images = models.ManyToManyField(ProductImage)

    def __str__(self):
        return self.name
    
class Advertisement(Timestamp):
    name = models.CharField(max_length=250)
    previous_price = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    Addcategory = models.ForeignKey(Addcategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Add/images/')

    def __str__(self):
        return self.name



class Review(Timestamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models. CharField(max_length=50)
    description = models.TextField()
    name = models.CharField(max_length=50)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    email = models.EmailField()
    profile = models.ImageField(upload_to='reviewer/profile/', default="")

    def __str__(self):
        return self.name
    
class Cart(Timestamp):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)  # For guest users
    is_active = models.BooleanField(default=True)  
    shipping_cost = models.IntegerField(default=0)
    discount_cost = models.IntegerField(default=0)

    def __str__(self):
        return f"Cart {self.id} - {'Guest' if not self.user else self.user.username}"

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total(self):
        return self.get_subtotal() + self.shipping_cost - self.discount_cost


class CartItem(Timestamp):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_total_price(self):
        return self.product.price * self.quantity

    


