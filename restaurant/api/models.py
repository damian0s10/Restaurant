from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, related_name = 'products', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    free_delivery = models.BooleanField(default=False)
    combines_with_others = models.BooleanField(default=True)
    active_from = models.DateTimeField(auto_now=False, auto_now_add=False)
    active_to = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.code


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=9)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    products = models.ManyToManyField(Product, related_name='order')
    discount_code = models.ForeignKey(DiscountCode, models.SET_NULL, blank=True, null=True, to_field='code')

    def get_products(self):
        return "\n".join([p.name for p in self.products.all()])


class OrderSummary(Order):
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    price_after_reduction = models.DecimalField(max_digits=5, decimal_places=2)
