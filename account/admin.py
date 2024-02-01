from django.contrib import admin

from .models import User, Seller, Customer, Company, Address

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Address)
