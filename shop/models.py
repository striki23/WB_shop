from django.db import models
from django.utils.translation import gettext_lazy as _
from pytils.translit import slugify
from django.core.validators import ValidationError, MinValueValidator
from django.contrib.auth.models import User

from my_utils.utils import validate_image, get_file_path
from shop.validators import ProductTitleValidator, ProfileImageValidator


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
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sale_price = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(
        'Фото',
        upload_to=get_file_path,
        default='shop/default.jpg',
        #     validators=[
        #         validate_image, ProfileImageValidator()
        #         ]
        # )
        validators=[validate_image]
    )
    is_available = models.BooleanField(default=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-is_available', '-time_update')

    def clean(self):
        if self.sale_price and self.sale_price >= self.price:
            raise ValidationError(
                f'Цена со скидкой не может быть больше либо равна '
                f'{self.price} руб.'
            )
        return super().clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(
        'Наименование баннера',
        max_length=255,
    )
    image = models.ImageField(
        'Баннер категории',
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

    def save(self, *args, **kwargs):
        self.title = f'Баннер {self.category} {self.pk}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    STARS_GOODS = (
        (1, '1-Отвратительно'),
        (2, '2-Плохо'),
        (3, '3-Удовлетворительно'),
        (4, '4-Хорошо'),
        (5, '5-Отлично'),
    )
    # TODO сделать отдельную модель grade - оценка

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )
    text = models.TextField('Ваш отзыв', blank=True)
    stars = models.IntegerField('Ваша оценка', choices=STARS_GOODS)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.stars}'
