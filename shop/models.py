from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from my_utils.utils import validate_image, get_file_path
from pytils.translit import slugify
from django.core.validators import ValidationError
from PIL import Image


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
            regex=r'[^a-zA-ZА-Яа-яЁё0-9,.%*() ]',
            message='Используйте буквы только латинского и русского алфавита',
            inverse_match=True
        )]
    )
    slug = models.SlugField(max_length=50, unique=True, null=False)
    description = models.TextField('Описание товара', max_length=600)
    price = models.PositiveIntegerField(default=0)
    sale_price = models.PositiveIntegerField(default=0, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-is_available', '-time_create')

    def clean(self):
        if self.sale_price >= self.price:
            raise ValidationError(f'Цена со скидкой не может быть больше либо равна {self.price} руб.')

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        width, height = img.size

        if width > 500 or height > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title
