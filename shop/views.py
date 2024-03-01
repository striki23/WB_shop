from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def index(request):
    products = Product.objects.all()
    return render(request, 'shop/products.html', context={'products': products})


def single_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products_in_cat = Product.objects.filter(category=category.pk)
    return render(request, 'shop/single_category.html', {'category': category, 'products_in_cat': products_in_cat})


def single_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'shop/single_product.html', {'product': product})


def page_404(request, exception):
    return render(request, 'shop/404.html', status=404)
