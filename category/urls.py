from django.urls import path

from .views import CategoryListView, SubCategoryListView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>', SubCategoryListView.as_view(), name='sub_category_list'),
]