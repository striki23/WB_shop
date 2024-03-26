from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    MALE_CHOICE = (
        ('Жен', 'Женский'),
        ('Муж', 'Мужской')
    )
    email = models.EmailField('Почтовый ящик', unique=True, blank=False, null=False)
    date_birth = models.DateTimeField('Дата рождения', blank=True, null=True)
    male = models.CharField('Пол', choices=MALE_CHOICE, max_length=7)
    phone_number = models.CharField(max_length=12,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{11,11}$',
            message="Номер телефона должен быть введен в формате: '+79999999999'")],
        unique=True
    )
