from django.test import TestCase, Client
from django.urls import reverse
from customer.models import Customer
from estimates.models import Estimate
from estimates.services import accept_estimate
from jobs.models import Job
from datetime import date


class EstimateModelTestCase(TestCase):
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

    def test_estimate_status_choices(self):
        valid_statuses = ['pending', 'accepted', 'rejected']
        for status in valid_statuses:
            estimate = Estimate.objects.create(
                customer=self.customer,
                description=f"Test {status}",
                estimated_cost=500.00,
                visit_date=date(2024, 7, 1),
                status=status
            )
            self.assertEqual(estimate.status, status)


class EstimateAcceptServiceTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            description="Service test estimate",
            estimated_cost=2000.00,
            visit_date=date(2024, 8, 1),
            status="pending"
        )

    def test_accept_estimate_creates_job(self):
        self.assertFalse(Job.objects.filter(estimate=self.estimate).exists())
        accept_estimate(self.estimate)

        self.estimate.refresh_from_db()
        self.assertEqual(self.estimate.status, 'accepted')

        job = Job.objects.get(estimate=self.estimate)
        self.assertIsNotNone(job)
        self.assertEqual(job.start_date, self.estimate.visit_date)
        self.assertEqual(job.status, 'scheduled')

    def test_accept_estimate_idempotent(self):
        accept_estimate(self.estimate)
        job_first = Job.objects.get(estimate=self.estimate)

        accept_estimate(self.estimate)
        jobs_count = Job.objects.filter(estimate=self.estimate).count()
        self.assertEqual(jobs_count, 1)


class EstimateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer1 = Customer.objects.create(
            name="Customer One",
            email="customer1@example.com"
        )
        self.customer2 = Customer.objects.create(
            name="Customer Two",
            email="customer2@example.com"
        )
        self.estimate1 = Estimate.objects.create(
            customer=self.customer1,
            description="First estimate",
            estimated_cost=5000.00,
            visit_date=date(2024, 9, 1),
            status="pending"
        )
        self.estimate2 = Estimate.objects.create(
            customer=self.customer2,
            description="Second estimate",
            estimated_cost=8000.00,
            visit_date=date(2024, 9, 15),
            status="accepted"
        )

    def test_estimate_list_view(self):
        response = self.client.get(reverse('estimate-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'estimates/list.html')
        self.assertContains(response, 'Customer One')
        self.assertContains(response, 'Customer Two')
        self.assertEqual(len(response.context['estimates']), 2)

    def test_estimate_create_view_get(self):
        response = self.client.get(reverse('estimate-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'estimates/estimate_form.html')

    def test_estimate_create_view_post_valid(self):
        data = {
            'customer': self.customer1.id,
            'description': 'New test estimate',
            'visit_date': '2024-10-01',
            'estimated_cost': '3500.00'
        }
        response = self.client.post(reverse('estimate-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Estimate.objects.count(), 3)

        new_estimate = Estimate.objects.latest('id')
        self.assertEqual(new_estimate.description, 'New test estimate')
        self.assertEqual(new_estimate.status, 'pending')

    def test_estimate_create_view_post_invalid(self):
        data = {
            'customer': self.customer1.id,
            'description': '',
            'visit_date': '',
            'estimated_cost': ''
        }
        response = self.client.post(reverse('estimate-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Estimate.objects.count(), 2)

    def test_estimate_accept_view_post(self):
        response = self.client.post(
            reverse('estimate-accept', args=[self.estimate1.id])
        )
        self.assertEqual(response.status_code, 302)

        self.estimate1.refresh_from_db()
        self.assertEqual(self.estimate1.status, 'accepted')
        self.assertTrue(Job.objects.filter(estimate=self.estimate1).exists())

    def test_estimate_accept_view_get_redirects(self):
        response = self.client.get(
            reverse('estimate-accept', args=[self.estimate1.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_estimate_accept_already_accepted(self):
        response = self.client.post(
            reverse('estimate-accept', args=[self.estimate2.id])
        )
        self.assertEqual(response.status_code, 302)
