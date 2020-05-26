from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, DiscountCode
from .rules import ProductDiscount
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer


class CategoryModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CheckDiscountCode(APIView):

    def get(self, request):
        code = request.query_params.get('code')
        try:
            discount_code = DiscountCode.objects.get(code=code)
        except DiscountCode.DoesNotExist:
            return Response({"code_exist": "False"})
        return Response({"code_exist": "True"})


class OrderFoodAPIView(APIView):
    def parse_data(self, data):
        data = [dict(fact.items()) for fact in data.facts.values()]
        data.pop(0)  # Remove first item
        return data

    def post(self, *args, **kwargs):
        products = list(sorted(self.request.data, key=lambda product: product['price']))
        products = OrderSerializer(products, many=True).data

        product_discount = ProductDiscount(products)
        product_discount.reset()
        product_discount.run()

        data = self.parse_data(product_discount)
        return Response({'data': data})
