from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, ProductCategory, WishlistItem
from rest_framework.test import APIClient
from rest_framework import status



class WishlistItemTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', password='testpass')
        self.category = ProductCategory.objects.create(name='TestCategory')
        self.product1 = Product.objects.create(name='Test Product 1', price='10.00', rank=4.5, user=self.user, category=self.category)
        self.product2 = Product.objects.create(name='Test Product 2', price='20.00', rank=4.0, user=self.user, category=self.category)

    def test_save(self):
        # Test adding the first product from the category
        wishlist_item1 = WishlistItem.objects.create(user=self.user, product=self.product1)
        self.assertEqual(wishlist_item1.user, self.user)
        self.assertEqual(wishlist_item1.product, self.product1)

        # Test adding a second product from the same category
        with self.assertRaises(ValidationError):
            WishlistItem.objects.create(user=self.user, product=self.product2)

from django.test import TestCase
from .models import Product
from .serializers import ProductSerializer

class ProductSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('testuser', password='testpass')
        self.category = ProductCategory.objects.create(name='TestCategory')
        self.product = Product.objects.create(name='Test Product 1', price='10.00', rank=4.5, user=self.user, category=self.category)
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['pk', 'name', 'user', 'price', 'category', 'created_time'])

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.product.name)

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], self.product.price)


    def test_read_only_fields(self):
        self.assertTrue(self.serializer.fields['created_time'].read_only)

