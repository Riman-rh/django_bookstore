from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Book, Review, Order, OrderItem, Shipping


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(ModelAdmin):
    model = Book
    list_display = [
        'title',
        'author'
    ]
    inlines = [ReviewInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class ShippingInline(admin.TabularInline):
    model = Shipping


class OrderAdmin(ModelAdmin):
    model = Order
    inlines = [OrderItemInline, ShippingInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)