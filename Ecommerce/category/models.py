from django.db import models
from django.urls import reverse

# Create your models here.
# user_name = Ecommerce
# password = Ecommerce1234


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=250, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args = [self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

