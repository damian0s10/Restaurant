from rest_framework import serializers
from .models import Product, Category, DiscountCode, Order

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'

    
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    
    class Meta:
        model = Category
        fields = '__all__'

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Order
        fields = '__all__'
