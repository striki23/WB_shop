from django.conf.urls.static import static
from django.urls import path

from wb_shop_root import settings
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductsHome.as_view(), name='index'),
    path('search', views.search_products, name='search_products'),
    path('<slug:product_slug>', views.SingleProduct.as_view(), name='single_product'),
    path('<slug:product_slug>/add_review', views.AddReview.as_view(), name='add_review'),
    path('categories/<slug:category_slug>', views.ProductsInCategory.as_view(), name='single_category')

]

handler404 = views.page_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
