from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer

class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')

    def test_get_all_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_category_by_normaluser(self):
        url = reverse('category-detail', kwargs={'pk': self.category1.pk})
        response = self.client.get(url)
        category = Category.objects.get(pk=self.category1.pk)
        serializer = CategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_category_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('category-detail', kwargs={'pk': self.category1.pk})
        response = self.client.get(url)
        category = Category.objects.get(pk=self.category1.pk)
        serializer = CategorySerializer(category)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_category_by_normaluser(self):
        url = reverse('category-list')
        data = {'name': 'new_category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('category-list')
        data = {'name': 'new_category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_update_category_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('category-detail', kwargs={'pk': self.category1.pk})
        data = {'name': 'category_update'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'category_update')

    def test_delete_category_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('category-detail', kwargs={'pk': self.category1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')
        self.product1 = Product.objects.create(name='product1', category=self.category1, price=10, imgsrc='')
        self.product2 = Product.objects.create(name='product2', category=self.category2, price=20, imgsrc='')
        self.product3 = Product.objects.create(name='product3', category=self.category1, price=30, imgsrc='')

    def test_get_products_of_category_by_normaluser(self):
        url = reverse('product-list-by-category', kwargs={'category_name': self.category1.name})
        response = self.client.get(url)
        products_of_category1 = Product.objects.filter(category=self.category1.id)
        serializer = ProductSerializer(products_of_category1, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_get_all_products_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-list')
        response = self.client.get(url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_category_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})
        response = self.client.get(url)
        product = Product.objects.get(pk=self.product1.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_product_by_normaluser(self):
        url = reverse('product-list')
        data = {'name': 'new_product', 'category': self.category1, 'price': 10, 'imgsrc': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-list')
        data = {'name': 'new_product', 'category': self.category1.name, 'price': 10, 'imgsrc': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 4)

    def test_update_product_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})
        data = {'name': 'product_update', 'category': self.category1.name, 'price': 10, 'imgsrc': ''}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'product_update')

    def test_delete_product_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 2)
