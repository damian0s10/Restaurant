from django.contrib import admin
from .models import Product, Category, DiscountCode, Order, OrderSummary

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']

class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ProductInline]

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'combines_with_others', 'active_from', 'active_to']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'phone_number', 'email', 'city', 'street', 
                    'house_number', 'get_products', 'discount_code']

@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'phone_number', 'email', 'city', 'street', 
                    'house_number', 'get_products', 'discount_code', 'total_price', 'price_after_reduction']