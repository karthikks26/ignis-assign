from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'category', 'url', 'image_url', 'title', 'price', 'mrp', 
            'last_7_day_sale', 'available_skus', 'fit', 'fabric', 
            'neck', 'sleeve', 'pattern', 'length', 'description',
            'category_image_url'
        ]
