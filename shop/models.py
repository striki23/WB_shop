from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=50, default='default_slug')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(max_length=600, verbose_name='Описание товара')
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/', default='shop/default.jpg', verbose_name='Фото')
    is_available = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
