from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'male', 'date_birth')
    #readonly_fields = ('time_create', 'slug')
    #search_fields = ('title', 'category__title')
    #list_editable = ('sale_price', 'is_available')
