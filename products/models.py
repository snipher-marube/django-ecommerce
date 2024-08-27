from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Represents a product category.
    """
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        
    def __str__(self):
        return self.category_name
    
    def get_absolute_url(self):
        return reverse('category_products', args=[self.slug])


class Product(models.Model):
    """
    Represents a product with details like name, description, price, and stock.
    """
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='uploads/images/products/%Y/%m/%d/')
    stock = models.PositiveBigIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def average_review(self):
        """
        Calculates the average rating for the product.
        """
        reviews = ReviewRating.objects.filter(product=self, status=True)
        average = reviews.aggregate(average=models.Avg('rating'))
        return float(average['average']) if average['average'] is not None else 0
    
    def count_review(self):
        """
        Counts the number of reviews for the product.
        """
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=models.Count('id'))
        return int(reviews['count']) if reviews['count'] is not None else 0


class VariationCategory(models.Model):
    """
    Represents a category of product variations (e.g., size, color).
    """
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Variation Category'
        verbose_name_plural = 'Variation Categories'
        indexes = [
            models.Index(fields=['id', 'name']),
        ]

    def __str__(self):
        return self.display_name


class Variation(models.Model):
    """
    Represents a specific variation of a product (e.g., Red, Large).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.ForeignKey(VariationCategory, on_delete=models.CASCADE, related_name='variations')
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        indexes = [
            models.Index(fields=['id', 'variation_category']),
        ]

    def __str__(self):
        return f'{self.variation_value} ({self.variation_category})'


class ProductGallery(models.Model):
    """
    Represents a gallery of images for a product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='uploads/images/products/gallery/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Gallery'

    def __str__(self):
        return f'Gallery for {self.product.product_name}'


class ReviewRating(models.Model):
    """
    Represents a review and rating given by a user for a product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review & Rating'
        verbose_name_plural = 'Reviews & Ratings'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.product_name}'
