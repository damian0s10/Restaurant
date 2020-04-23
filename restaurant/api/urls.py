from django.urls import path
from .views import CategoryModelViewSet, ProductModelViewSet, OrderViewSet, CheckDiscountCode
from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter()
router.register(r'categories', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)
router.register(r'orders', OrderViewSet, basename="OrderModelViewSet")


urlpatterns = [
    path('discount-code/', CheckDiscountCode.as_view()),
    path('', include(router.urls)),
]