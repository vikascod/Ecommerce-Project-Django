from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

# Create your models here.
STATE_CHOICES = (
    ('Delhi', 'Delhi'),
    ('Mumbai', 'Mumbai'),
    ('Goa', 'Goa'),
    ('Chennai', 'Chennai'),
    ('Kolkata', 'Kolkata'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    zip_code = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)


    def __str__(self):
        return str(self.id)
    

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
    def update_rating(self):
        self.rating = self.rating_set.aggregate(Avg('rating'))['rating__avg']
        self.save()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cencal', 'Cencal'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='Pending')

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)



class FreqenltyAskQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question[:30]


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])


    # def update_rating(self):
    #     product = self.product
    #     product.rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    #     product.save()
        
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.update_rating()
