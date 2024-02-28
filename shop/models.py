from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(_('Название'), max_length=255)
    slug = models.SlugField(max_length=50)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

# TODO как создать бэкап БД

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

# TODO добавить валидатор для названия image (from uuid import uuid4)
# TODO ограничить допустимые форматы картинок
# TODO ограничить размер и разрешение картинок
# TODO проверка title(только рус, англ)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-is_available', '-time_create')

    def __str__(self):
        return self.title
