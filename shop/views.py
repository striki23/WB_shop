# Встроенные модули
# import os
# from abc import ABC

# Внешние модули
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

# Модули проекта
from shop.models import Product, Category


def index(request):
    products = Product.objects.all().annotate(
        sale=(F('price') - F('sale_price')) * 100 / F('price')
    )
    return render(
        request,
        'shop/products.html',
        context={'products': products}
    )


def search_products(request):
    if request.method == 'POST' and request.POST.get('searched'):
        # r_search = request.POST.get('searched')
        r_search = request.POST['searched']
        products = Product.objects.filter(title__icontains=r_search).annotate(
            sale=(F('price') - F('sale_price')) * 100 / F('price')
        )
        return render(
            request,
            'shop/search_products.html',
            context={'products': products, 'r_search': r_search}
        )
    # TODO: return redirect('index', permanent=True)


# TODO: cat_selected возможно не используется
def single_category(request, category_slug, cat_selected=0):
    category = get_object_or_404(Category, slug=category_slug)
    products_in_cat = category.products.annotate(
            sale=(F('price') - F('sale_price')) * 100 / F('price')
        )
    banners = category.banners.all()
    # TODO: Возможно передаются ненужные данные в контексте запроса
    context = {
        'category': category,
        'products_in_cat': products_in_cat,
        'cat_selected': category.pk,
        'banners': banners,
    }
    return render(
        request,
        'shop/single_category.html',
        context=context
    )


def single_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(
        request,
        'shop/single_product.html',
        {'product': product}
    )


def page_404(request, exception):
    return render(
        request,
        'shop/404.html',
        status=404
    )
