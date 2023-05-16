from django.test import TestCase
from django.db import IntegrityError
from products.models import Category, Product

class CategoryTest(TestCase):
    def test_categoryname_unique(self):
        Category.objects.create(name='testname')
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='testname')
