from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

class Cover(models.Model):
    cover_title         = models.CharField(max_length=20, blank=True)
    cover_description   = models.CharField(max_length=30, blank=True)
    cover_image         = models.ImageField(upload_to='photos/covers')

    def __str__(self):
        return self.cover_title

class Product(models.Model):
    product_name        = models.CharField(max_length=50, unique=True, verbose_name='Наименование товара')
    slug                = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')
    description         = models.TextField(max_length=500, blank=True, verbose_name='Описание')
    old_price           = models.IntegerField(verbose_name='Старая цена')
    price               = models.IntegerField(verbose_name='Цена')
    images              = models.ImageField(upload_to='photos/products', verbose_name='Картинки')
    stock               = models.IntegerField(verbose_name='Склад')
    is_available        = models.BooleanField(default=True, verbose_name='Доступен')
    is_popular          = models.BooleanField(default=False, verbose_name='Популярен')
    is_newarrived       = models.BooleanField(default=False, verbose_name='Новый')
    is_recommended      = models.BooleanField(default=False, verbose_name='Рекомендовано')
    category            = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    created_date        = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date       = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product = self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product = self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active=True)
    
    def colors(self):
         return super(VariationManager, self).filter(variation_category = 'color', is_active=True)


variation_category_choice = (
    ('size', 'size'),
    ('color', 'color'),
)

class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    user                = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject             = models.CharField(max_length=100, blank=True)
    review              = models.CharField(max_length=500, blank=True)
    rating              = models.FloatField()
    ip                  = models.CharField(max_length=20, blank=True)
    status              = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product     = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image       = models.ImageField(upload_to = 'store/products', max_length = 255)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

