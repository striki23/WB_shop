from django.contrib import admin
from .models import Category, Product, Banner


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'sale_price', 'category', 'is_available', )
    readonly_fields = ('time_create', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class BannerAdmin(admin.ModelAdmin):
    list_display = ('image', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
