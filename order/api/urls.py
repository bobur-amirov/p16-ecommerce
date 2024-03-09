from django.urls import path

from .views import OrderListView, AddOrderView, RemoveOrderView, OrderItemIncremintAPIView, OrderItemDecrementAPIView

urlpatterns = [
    path('order/', OrderListView.as_view(), name='order_list'),
    path('order/add/<int:pk>', AddOrderView.as_view(), name='add_order'),
    path('order/remove/<int:pk>', RemoveOrderView.as_view(), name='remove_order'),
    path('order/increment/<int:pk>', OrderItemIncremintAPIView.as_view(), name='order_inc'),
    path('order/decrement/<int:pk>', OrderItemDecrementAPIView.as_view(), name='order_dec'),
]