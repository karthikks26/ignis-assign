from rest_framework import viewsets
from products.models import Product
from products.serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
