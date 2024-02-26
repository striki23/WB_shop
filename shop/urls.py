from django.conf.urls.static import static
from django.urls import path

from wb_shop_root import settings
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>', views.single_product, name='single_product'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:category_slug>', views.single_category, name='single_category')
    # не понимаю до конца как он находит 'category_slug'
]

handler404 = views.page_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
