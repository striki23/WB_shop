from django.contrib import admin
from .models import Category, Product, Banner


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'sale_price', 'category', 'is_available', )
    readonly_fields = ('time_create', 'slug')
    search_fields = ('title', 'category__title')
    list_editable = ('sale_price', 'is_available')
    list_per_page = 10
    actions = ['set_available', 'set_not_available']

    @admin.action(description='Товар доступен к заказу')
    def set_available(self, request, queryset):
        count = queryset.update(is_available=True)
        self.message_user(request, message=f'Изменено {count} записей')

    @admin.action(description='Товар недоступен к заказу')
    def set_not_available(self, request, queryset):
        count = queryset.update(is_available=False)
        self.message_user(request, message=f'Изменено {count} записей')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
