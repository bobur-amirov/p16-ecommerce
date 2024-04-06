from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from order.api.permissions import OrderPermission, OrderItemAuthorPermission
from order.api.serializers import OrderSerializer
from order.models import Order, OrderItem
from order.services import inc_or_dec
from order.tasks import send_email
from product.models import Product


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class AddOrderView(APIView):
    # permission_classes = [permissions.IsAuthenticated, OrderPermission]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, product)
        if product.quantity <= 0:
            return Response({'message': "Product qolmadi!"}, status=status.HTTP_200_OK)
        order, created = Order.objects.get_or_create(customer=request.user, ordered=False)
        if created:
            send_email.delay(order.id)
        orderitem, item_created = OrderItem.objects.get_or_create(product=product, customer=request.user, ordered=False)
        if not item_created:
            orderitem.quantity = F('quantity') + 1
            orderitem.save()
            product.quantity = F('quantity') - 1
            product.save()
        else:
            order.orderitem.add(orderitem)
            product.quantity = F('quantity') - 1
            product.save()
        return Response({"message": "Ok"}, status=status.HTTP_201_CREATED)


class RemoveOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        order = Order.objects.filter(orderitem=orderitem, ordered=False).first()
        self.check_object_permissions(self.request, orderitem)
        orderitem.product.quantity = F('quantity') + F('orderitem.quantity')
        orderitem.product.save()
        order.orderitem.remove(orderitem)
        orderitem.delete()
        return Response({"message": 'Ok'}, status=status.HTTP_204_NO_CONTENT)


class OrderItemIncremintAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(self.request, orderitem)
        if orderitem.product.quantity <= 0:
            return Response({'message': "Product qolmadi!"}, status=status.HTTP_200_OK)
        inc_or_dec(obj=orderitem, num=1, is_inc=True)
        inc_or_dec(obj=orderitem.product, num=1, is_inc=False)
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)


class OrderItemDecrementAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(self.request, orderitem)
        if orderitem.quantity == 1:
            orderitem.product.quantity = F('quantity') + 1
            orderitem.product.save()
            orderitem.delete()
            return Response({'message': "Order deleted"}, status=status.HTTP_204_NO_CONTENT)
        orderitem.quantity = F('quantity') + 1
        orderitem.save()
        orderitem.product.quantity = F('quantity') + 1
        orderitem.product.save()
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)
