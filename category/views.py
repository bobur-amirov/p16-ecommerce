from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Category
from product.models import Product


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category/category_list.html'

    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        return qs.filter(parent=None)

class SubCategoryListView(ListView):
    model = Category
    context_object_name = 'sub_categories'
    template_name = 'category/sub_category_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        qs = super().get_queryset()
        return qs.filter(parent__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs['slug']

        context['products'] = Product.objects.filter(Q(category__slug=slug) |
                                                     Q(category__parent__slug=slug))

        return context


