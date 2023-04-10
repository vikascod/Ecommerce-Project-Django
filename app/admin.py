from django.contrib import admin
from app.models import Cart, Customer, Product, OrderPlaced, FreqenltyAskQuestion, Rating
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zip_code', 'state']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'discount_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'customer_info', 'product_info', 'product', 'quantity', 'ordered_date', 'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)


    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

admin.site.register(FreqenltyAskQuestion)
admin.site.register(Rating)