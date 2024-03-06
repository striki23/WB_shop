from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.db.models import F
import math


def index(request):
    products = Product.objects.all().annotate(sale=(F('price') - F('sale_price')) * 100 / F('price'))
    return render(request, 'shop/products.html', context={'products': products})


def search_products(request):
    if request.method == 'POST' and request.POST['searched'] != '':
        r_search = request.POST['searched']
        products = Product.objects.filter(title__icontains=r_search)
        return render(request, 'shop/search_products.html', context={'products': products, 'r_search': r_search})
    return redirect('index', permanent=True)


def single_category(request, category_slug, cat_selected=0):
    category = get_object_or_404(Category, slug=category_slug)
    products_in_cat = category.products
    context = {
        'category': category,
        'products_in_cat': products_in_cat,
        'cat_selected': category.pk
    }
    return render(request, 'shop/single_category.html', context=context)


def single_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'shop/single_product.html', {'product': product})


def page_404(request, exception):
    return render(request, 'shop/404.html', status=404)
