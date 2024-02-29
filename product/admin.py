from django.contrib import admin

from product.models import Product, Images, Color, Size

# Register your models here.

admin.site.register(Images)
admin.site.register(Color)
admin.site.register(Size)


class ItemInline(admin.StackedInline):
    model = Images
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'quantity', 'category']
    prepopulated_fields = {'slug': ('title', 'category'), }
    inlines = [ItemInline]
