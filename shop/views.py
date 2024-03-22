# Встроенные модули
# import os
# from abc import ABC

# Внешние модули
from django.db.models import Avg, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Модули проекта
from shop.models import Product, Category, Review
from shop.forms import AddReviewForm


class ProductsHome(ListView):
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.all().annotate(
            sale=(F('price') - F('sale_price')) * 100 / F('price')
        )


class SearchProducts(ListView):
    model = Product
    template_name = 'shop/search_products.html'
    context_object_name = 'products'
    # extra_context = {'query': request.GET.get('q')}
    # TODO как здесь получить request

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Product.objects.filter(Q(title__icontains=query)).annotate(
             sale=(F('price') - F('sale_price')) * 100 / F('price')
         )
        return queryset


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
        if context['products_in_cat']:
            first_prod, *_ = context['products_in_cat']
            category = first_prod.category
            context['category'] = category
            context['cat_selected'] = category.pk
            context['banners'] = category.banners.all()
            return context
        context['empty'] = 'В данной категории еще нет товаров...'
        return context


class ShowProductMixin(DetailView):
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['reviews'] = product.reviews.all()
        if context['reviews']:
            avg_review_stars = product.reviews.aggregate(Avg("stars")).get('stars__avg', 0)
            context['avg_review_stars'] = round(avg_review_stars, 1)
        return context


class SingleProduct(ShowProductMixin):
    template_name = 'shop/single_product.html'


class AddReview(LoginRequiredMixin, ShowProductMixin, FormView):
    template_name = 'shop/add_review_for_product.html'
    form_class = AddReviewForm

    def get_success_url(self):
        return reverse_lazy(
            'shop:single_product',
            kwargs={"product_slug": self.kwargs.get('product_slug')}
        )

    def form_valid(self, form):
        form.instance.product_id = Product.objects.get(
            slug=self.kwargs.get('product_slug')).pk
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


def page_404(request, exception):
    return render(
        request,
        'shop/404.html',
        status=404
    )
