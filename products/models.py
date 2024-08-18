from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images')
    stock = models.PositiveBigIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/gallery')
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Gallery'
        
