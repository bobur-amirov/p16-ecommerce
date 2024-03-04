from django.db import models

from base.models import TimeStampedModel
from account.models import User
from product.models import Product


class OrderItem(TimeStampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} * {self.product.price} = {self.total_price}'


class Order(TimeStampedModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order = models.ManyToManyField(OrderItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.total_price}'
