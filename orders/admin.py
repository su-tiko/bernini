from django.contrib import admin
from .models import Order
from .forms import UserAdminAuthenticationForm


class UserAdminSite(admin.AdminSite):
    site_header = 'Bernini Online Shop'
    site_title = 'Buy your new shoes'
    index_title = 'Place your order'
    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        super().has_permission(request)
        return request.user.is_active


class OrderInline(admin.TabularInline):
    model = Order.products.through


class UserOrderInline(admin.TabularInline):
    model = Order.products.through
    readonly_fields = ['total']

    def has_module_permission(self, request):
        return request.user.is_active

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_active and (obj is None or obj.client == request.user)

    def has_add_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_active and (obj is None or obj.client == request.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_active and (obj is None or obj.client == request.user)

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_active and (obj is None or obj.client == request.user)

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_staff or request.user.is_active and (obj is None or obj.client == request.user)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total_items', 'total_price', 'created']
    inlines = [
        OrderInline
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)


class UserOrderAdmin(OrderAdmin):
    exclude = ['client']
    inlines = [
        UserOrderInline
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs

        return qs.filter(client=request.user)

    def save_model(self, request, obj, form, change):
        obj.client = request.user
        obj.save()

    def has_add_permission(self, request):
        return request.user.is_active

    def has_module_permission(self, request):
        return request.user.is_active

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active and (obj is None or obj.client == request.user)

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_active and (obj is None or obj.client == request.user)

    def has_change_permission(self, request, obj=None):
        return self.has_view_or_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        return self.has_view_or_change_permission(request, obj)


user_admin = UserAdminSite(name='users-admin')

admin.site.register(Order, OrderAdmin)
user_admin.register(Order, UserOrderAdmin)
