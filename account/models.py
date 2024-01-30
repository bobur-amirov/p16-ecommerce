from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'seller'),
      (3, 'custumer'),
  )
  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
  phone_number = models.CharField(max_length=13)

  def __str__(self):
      return self.username

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    text = models.CharField(max_length=225)

    def __str__(self):
        return self.text[:10]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='customer', null=True)

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller', null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='seller', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='seller', null=True)

    def __str__(self):
        return self.user.username
