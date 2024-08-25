from django.db import models
from django.forms import ValidationError
from django.urls import reverse

class Category(models.Model):
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
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/')
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
class VariationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)  # For displaying in the choices
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = 'Variation Category'
        verbose_name_plural = 'Variation Categories'
        indexes = [
            models.Index(fields=['id', 'name']),
        ]

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.ForeignKey(VariationCategory, on_delete=models.CASCADE)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.variation_value} ({self.variation_category})'
    
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        indexes = [
            models.Index(fields=['id', 'variation_category']),
        ]
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/%Y/%m/%d/')
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Gallery'
        
