import os
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from PIL import Image
from my_utils.utils import validate_image, get_file_path


class Category(models.Model):
    title = models.CharField(_('Название'), max_length=255, unique=True)
    slug = models.SlugField(max_length=50)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        'Название',
        max_length=255,
        unique=True,
        validators=[RegexValidator(
            regex=r'[^a-zA-ZА-Яа-яЁё0-9 ]',
            message='Используйте буквы только латинского и русского алфавита',
            inverse_match=True
        )]
    )
    slug = models.SlugField(max_length=50)
    description = models.TextField('Описание товара', max_length=600)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField('Фото',
                              upload_to=get_file_path,
                              default='shop/default.jpg',
                              validators=[validate_image,
                                          FileExtensionValidator(
                                              allowed_extensions=['jpg', 'png', 'jpeg'],
                                              message='Данный формат файла не поддерживается', )]
                              )
    is_available = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    # добавить валидатор для названия image (from uuid import uuid4) - готово
    # ограничить допустимые форматы картинок - готово
    # ограничить размер и разрешение картинок - готово
    # проверка title(только рус, англ) - готово

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-is_available', '-time_create')

    # сохраняем все изображение в разрешении 300*300 и меньше
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        width, height = img.size

        if width > 500 or height > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title
