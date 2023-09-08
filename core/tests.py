from django.test import TestCase
import unittest
from .models import Business, Product
from django.contrib.auth.models import User
# Create your tests here.


class BusinessTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        user = User.objects.create_user(username='mezard', password='mezard2001')
        userx = User.objects.get(username='mezard')
        Business.objects.create(business_name='Knits by Zarah', user=userx, slug='Knits-by-zarah')

    def test_your_model_method(self):
        obj = Business.objects.get(business_name='Knits by Zarah')

        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), obj.business_name)
        print(obj.business_name)


class ProductTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        
        user = User.objects.create_user(username='mezard', password='mezard2001')
        userx = User.objects.get(username='mezard')
        biz = Business.objects.create(business_name='Knits by Zarah', user=userx, slug='Knits-by-zarah')
        Product.objects.create(product_name='Knits by Zarah', business=biz, slug='Knits-by-zarah', product_description='Sellers can create listings and manage their shops from the dashboard', 
                               product_terms='terms', product_price=456, product_redirect_url='https://chat.openai.com/c/82529add-24a0-4ce2-b002-a5a8cd4e3348',
                               product_image='/static/images/dots.png', status='Active')

    def test_your_model_method(self):
        obj = Product.objects.get(product_name='Knits by Zarah')

        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), obj.product_name )
        print(obj.product_name)