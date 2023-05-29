from django.db import models
from accounts.models import Account
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

