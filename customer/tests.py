from django.test import TestCase

import customer
from customer.models import Customer


class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(name="Maina Geofrey", email="mainageofrey@gmail.com",
                                phone_number="0742954545", address="Nairobi, Kenya")

    def test_customer_creation(self):
        customer = Customer.objects.get(name="Maina Geofrey")
        self.assertEqual(customer.email, "mainageofrey@gmail.com")

    def test_customer_str_representation(self):
        customer = Customer.objects.get(name="Maina Geofrey")
        self.assertEqual(str(customer), "Maina Geofrey")
