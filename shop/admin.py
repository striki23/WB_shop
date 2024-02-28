from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_available')
    readonly_fields = ('time_create',)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
