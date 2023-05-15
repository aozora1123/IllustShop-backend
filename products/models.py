from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    imgsrc = models.CharField(max_length=255, default='', null=True, blank=True)
