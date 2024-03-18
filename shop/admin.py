from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Banner, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'sale_price', 'category', 'is_available',)
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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'stars', 'text', 'product', 'review_image')

    @admin.display(description='Фото отзыва')
    def review_image(self, review: Review):
        if review.image:
            return mark_safe(
                f"<img class='image-detail' src='{ review.image.url }' width=50>"
            )
        return 'Без фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Review, ReviewAdmin)
