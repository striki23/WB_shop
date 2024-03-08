from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from pytils.translit import slugify
from django.core.validators import ValidationError
from PIL import Image

from my_utils.utils import validate_image, get_file_path
from shop.validators import ProductTitleValidator


class Category(models.Model):
    title = models.CharField(
        _('Название'),
        max_length=255,
        unique=True
    )
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
        validators=[ProductTitleValidator()]
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=False
    )
    description = models.TextField(
        'Описание товара', max_length=600
    )
    price = models.PositiveIntegerField(
        # TODO: Валидатор для обработки стоимости,
        #  нельзя стоимость 0 указывать
    )
    sale_price = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(
        'Фото',
        upload_to=get_file_path,
        default='shop/default.jpg',
        validators=[
            validate_image,
            FileExtensionValidator(
                allowed_extensions=['jpg', 'png', 'jpeg'],
                message='Данный формат файла не поддерживается',
            )]
    )
    is_available = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-is_available', '-time_update')

    def clean(self):
        if self.sale_price >= self.price:
            raise ValidationError(
                f'Цена со скидкой не может быть больше либо равна '
                f'{self.price} руб.'
            )
        return super().clean()

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)

        img = Image.open(self.image.path)
        width, height = img.size

        if width > 500 or height > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Banner(models.Model):
    # TODO: название баннера
    image = models.ImageField(
        'Банер категории',
        upload_to=get_file_path,
        default='shop/default.jpg'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='banners'
    )

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.category.title
