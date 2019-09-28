from django.contrib import admin
from .models import Order


class OrderInline(admin.TabularInline):
    model = Order.products.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total_price', 'created']
    inlines = [
        OrderInline
    ]


admin.site.register(Order, OrderAdmin)
