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

