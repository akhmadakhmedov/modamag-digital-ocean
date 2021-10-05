from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name           = models.CharField(max_length=50, unique=True, verbose_name='Категория')
    slug                    = models.SlugField(unique=True, max_length=100, verbose_name='Слаг')
    description             = models.TextField(max_length=255, blank=True, verbose_name='Описание')
    cat_image               = models.ImageField(upload_to = 'photos/categories', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
       return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
