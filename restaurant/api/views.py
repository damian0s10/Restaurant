from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, DiscountCodeSerializer
from .models import Category, Product, Order, DiscountCode
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

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
            return Response({"code_exist" : "False"})
        return Response({"code_exist" : "True"})
        

class OrderViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)