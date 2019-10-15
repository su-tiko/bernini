from django.contrib import admin

from .models import Product
from orders.admin import user_admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name', 'description')


class UserProductAdmin(ProductAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_active

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_active


admin.site.register(Product, ProductAdmin)
user_admin.register(Product, UserProductAdmin)
