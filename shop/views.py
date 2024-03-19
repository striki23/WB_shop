# Встроенные модули
# import os
# from abc import ABC

# Внешние модули
from django.db.models import F, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

# Модули проекта
from shop.models import Product, Category, Review
from shop.forms import AddReviewForm


# def index(request):
#     products = Product.objects.all().annotate(
#         sale=(F('price') - F('sale_price')) * 100 / F('price')
#     )
#
#     return render(
#         request,
#         'shop/products.html',
#         context={'products': products}
#     )

class ProductsHome(ListView):
    template_name = 'shop/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().annotate(
            sale=(F('price') - F('sale_price')) * 100 / F('price')
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


# def single_category(request, category_slug, cat_selected=0):
#     category = get_object_or_404(Category, slug=category_slug)
#     products_in_cat = category.products.annotate(
#         sale=(F('price') - F('sale_price')) * 100 / F('price')
#     )
#     banners = category.banners.all()
#     context = {
#         'category': category,
#         'products_in_cat': products_in_cat,
#         'cat_selected': category.pk,
#         'banners': banners,
#     }
#     return render(
#         request,
#         'shop/single_category.html',
#         context=context
#     )

class ProductsInCategory(ListView):
    template_name = 'shop/single_category.html'
    context_object_name = 'products_in_cat'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return category.products.annotate(
                sale=(F('price') - F('sale_price')) * 100 / F('price')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products_in_cat'][0].category
        context['category'] = category
        context['cat_selected'] = category.pk
        context['banners'] = category.banners.all()
        return context


# def single_product(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#     reviews = Review.objects.filter(product=product)
#     avg_review_stars_dict = product.reviews.aggregate(Avg("stars"))
#     avg_review_stars = avg_review_stars_dict['stars__avg']
#     data = {
#         'product': product,
#         'reviews': reviews,
#         'avg_review_stars': avg_review_stars
#     }
#     return render(
#         request,
#         'shop/single_product.html',
#         data
#     )


class SingleProduct(DetailView):
    model = Product
    template_name = 'shop/single_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['reviews'] = Review.objects.filter(product=product)
        avg_review_stars_dict = product.reviews.aggregate(Avg("stars"))
        avg_review_stars = avg_review_stars_dict['stars__avg']
        context['avg_review_stars'] = avg_review_stars
        return context


# def add_review_for_product(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#     if request.method == 'POST':
#         form = AddReviewForm(request.POST)
#         if form.is_valid():
#             try:
#                 Review.objects.create(product=product, **form.cleaned_data)
#                 return redirect('shop:single_product', product.slug)
#             except:
#                 form.add_error(None, 'Ошибка в создании отзыва')
#             # form.save()
#             # TODO: как передать при сохранении передать в форму product
#
#             return redirect('shop:single_product', product.slug)
#
#     else:
#         form = AddReviewForm()
#
#     data = {
#         'product': product,
#         'form': form
#     }
#     return render(
#         request,
#         'shop/add_review_for_product.html',
#         data
#     )


class AddReview(DetailView, FormView):
    model = Product
    template_name = 'shop/add_review_for_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form_class = AddReviewForm
    success_url = reverse_lazy('shop:index')

    def form_valid(self, form):
        form.save
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['reviews'] = Review.objects.filter(product=product)
        avg_review_stars_dict = product.reviews.aggregate(Avg("stars"))
        avg_review_stars = avg_review_stars_dict['stars__avg']
        context['avg_review_stars'] = avg_review_stars
        return context


def page_404(request, exception):
    return render(
        request,
        'shop/404.html',
        status=404
    )
