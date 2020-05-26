from rest_framework import serializers

from .models import Product, Category, DiscountCode


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'size']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']

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


class OrderSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    id = serializers.IntegerField()
    price = serializers.FloatField()
    category = serializers.SerializerMethodField(source='category')
    size = serializers.IntegerField()
    count = serializers.IntegerField()

    def get_category(self, obj):
        return obj.get('category').lower().strip()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
