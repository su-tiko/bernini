"""bernini URL Configuration
"""
from django.contrib import admin
from django.urls import path
from orders.admin import user_admin

urlpatterns = [
    path('', user_admin.urls),
    path('admin/', admin.site.urls)
]
