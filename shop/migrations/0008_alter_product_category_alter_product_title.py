# Generated by Django 4.0.8 on 2024-03-04 09:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(inverse_match=True, message='Используйте буквы только латинского и русского алфавита', regex='[^a-zA-ZА-Яа-яЁё0-9,.%*() ]')], verbose_name='Название'),
        ),
    ]
