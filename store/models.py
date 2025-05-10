from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('Cloths', 'Cloths'),
    ('Jewellery', 'Jewellery'),
    ('Shoes', 'Shoes'),
    ('Other', 'Other'),
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Optional image for product

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    title = models.CharField(max_length=100, null=True, blank=True)  # Optional title for each image

    def __str__(self):
        return f"Image for {self.product.name}"

class Feedback(models.Model):
    product = models.ForeignKey(Product, related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional, for anonymous feedback
    email = models.EmailField(blank=True, null=True)  # Optional, for anonymous feedback
    rating = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)  # Track when the feedback was created

    class Meta:
        ordering = ['-created_at']  # Newest feedback appears first

    def __str__(self):
        return self.name or f"Anonymous Feedback for {self.product.name}"

