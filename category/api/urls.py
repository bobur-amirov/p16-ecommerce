from django.urls import path


from .views import CategoryListView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category_list')
]