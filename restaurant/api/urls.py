from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryModelViewSet, ProductModelViewSet, CheckDiscountCode, OrderFoodAPIView

router = DefaultRouter()
router.register(r'categories', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('discount-code/', CheckDiscountCode.as_view()),
    path('make-order/', OrderFoodAPIView.as_view()),
    path('', include(router.urls)),
]
