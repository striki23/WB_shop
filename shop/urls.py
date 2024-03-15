from django.conf.urls.static import static
from django.urls import path

from wb_shop_root import settings
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_products, name='search_products'),
    path('<slug:product_slug>', views.single_product, name='single_product'),
    path('<slug:product_slug>/add_review', views.add_review_for_product, name='add_review'),
    path('categories/<slug:category_slug>', views.single_category, name='single_category')

]

handler404 = views.page_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
