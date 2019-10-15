from rest_framework import serializers, viewsets, permissions
from rest_framework.routers import DefaultRouter

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permission for allowing staff users to edit and delete and others to read_only
    """
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff


class Products(viewsets.ModelViewSet):
    """
    API endpoint for managing Products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]


router = DefaultRouter()
router.register(r'', Products)

