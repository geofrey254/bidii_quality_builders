from django.test import TestCase
from customer.models import Customer
from estimates.models import Estimate
# Create your tests here.


class EstimateTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Maina Geofrey",
            email="mainageofrey@gmail.com",
            phone_number="0742954545",
            address="Nairobi, Kenya"
        )
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            description="Test estimate",
            estimated_cost=1000.00,
            visit_date="2024-07-01",
            status="pending"
        )

    def test_estimate_creation(self):
        estimate = Estimate.objects.get(id=self.estimate.id)
        self.assertEqual(estimate.description, "Test estimate")
        self.assertEqual(estimate.estimated_cost, 1000.00)
        self.assertEqual(estimate.visit_date.strftime(
            "%Y-%m-%d"), "2024-07-01")
        self.assertEqual(estimate.status, "pending")
        self.assertEqual(estimate.customer.name, "Maina Geofrey")

    def test_estimate_str_representation(self):
        estimate = Estimate.objects.get(id=self.estimate.id)
        self.assertEqual(
            str(estimate), f"Estimate for {estimate.customer.name}")
