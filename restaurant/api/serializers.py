from rest_framework import serializers

from .models import Product, Category, DiscountCode, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'size']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'products']

    def create(self, validated_data):
        products = validated_data.pop('products')
        category = Category.objects.create(**validated_data)
        for product in products:
            Product.objects.create(category=category, **product)
        return category


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
