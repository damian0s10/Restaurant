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
    SMALL_SIZE = 1
    BIG_SIZE = 2

    SIZE_CHOICES = (
        (SMALL_SIZE, 'small size'),
        (BIG_SIZE, 'big size'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(choices=SIZE_CHOICES, default=BIG_SIZE)

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
