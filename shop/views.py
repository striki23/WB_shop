# Встроенные модули
# import os
# from abc import ABC

# Внешние модули
from django.db.models import F, Avg
from django.shortcuts import get_object_or_404, redirect, render

# Модули проекта
from shop.models import Product, Category, Review
from shop.forms import AddReviewForm


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
        r_search = request.POST['searched']
        products = Product.objects.filter(title__icontains=r_search).annotate(
            sale=(F('price') - F('sale_price')) * 100 / F('price')
        )
        return render(
            request,
            'shop/search_products.html',
            context={'products': products, 'r_search': r_search}
        )


def single_category(request, category_slug):
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
    reviews = Review.objects.filter(product=product)
    avg_review_stars_dict = product.reviews.aggregate(Avg("stars"))
    avg_review_stars = avg_review_stars_dict['stars__avg']
    data = {
        'product': product,
        'reviews': reviews,
        'avg_review_stars': avg_review_stars
    }
    return render(
        request,
        'shop/single_product.html',
        data
    )


def add_review_for_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    form = AddReviewForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        print(review.image)
        review.save()
        return redirect('shop:single_product', product.slug)

    data = {
        'product': product,
        'form': form
    }
    return render(
        request,
        'shop/add_review_for_product.html',
        data
    )


def page_404(request, exception):
    return render(
        request,
        'shop/404.html',
        status=404
    )
