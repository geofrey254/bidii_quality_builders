from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from decimal import Decimal
from customer.models import Customer
from estimates.models import Estimate
from jobs.models import Job
from invoices.models import Invoice


class DashboardHomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test data
        self.customer1 = Customer.objects.create(
            name="Dashboard Customer 1",
            email="dash1@example.com"
        )
        self.customer2 = Customer.objects.create(
            name="Dashboard Customer 2",
            email="dash2@example.com"
        )

        self.estimate1 = Estimate.objects.create(
            customer=self.customer1,
            description="Dashboard estimate 1",
            estimated_cost=Decimal('5000.00'),
            visit_date=date(2024, 12, 1),
            status="accepted"
        )
        self.estimate2 = Estimate.objects.create(
            customer=self.customer2,
            description="Dashboard estimate 2",
            estimated_cost=Decimal('3000.00'),
            visit_date=date(2024, 12, 15),
            status="pending"
        )

        self.job1 = Job.objects.create(
            estimate=self.estimate1,
            start_date=date(2024, 12, 1),
            end_date=date(2024, 12, 5),
            status='completed'
        )
        self.job2 = Job.objects.create(
            estimate=self.estimate2,
            start_date=date(2024, 12, 15),
            status='scheduled'
        )

        self.invoice1 = Invoice.objects.create(
            job=self.job1,
            total_amount=Decimal('5000.00'),
            due_date=date(2025, 1, 15),
            paid=True
        )
        self.invoice2 = Invoice.objects.create(
            job=self.job2,
            total_amount=Decimal('3000.00'),
            due_date=date(2025, 1, 1),
            paid=False
        )

    def test_dashboard_view_GET(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

    def test_dashboard_context_total_customers(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_customers'], 2)

    def test_dashboard_context_total_estimates(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_estimates'], 2)

    def test_dashboard_context_accepted_estimates(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['accepted_estimates'], 1)

    def test_dashboard_context_total_jobs(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_jobs'], 2)

    def test_dashboard_context_completed_jobs(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['completed_jobs'], 1)

    def test_dashboard_context_total_invoices(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_invoices'], 2)

    def test_dashboard_context_paid_invoices(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['paid_invoices'], 1)

    def test_dashboard_context_paid_revenue(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['paid_revenue'], Decimal('5000.00'))

    def test_dashboard_context_outstanding_revenue(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(
            response.context['outstanding_revenue'], Decimal('3000.00'))

    def test_dashboard_has_revenue_chart(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertIn('revenue_chart', response.context)
        self.assertIsNotNone(response.context['revenue_chart'])

    def test_dashboard_has_job_status_chart(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertIn('job_status_chart', response.context)
        self.assertIsNotNone(response.context['job_status_chart'])


class DashboardEmptyStateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_empty_customers(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_customers'], 0)

    def test_dashboard_empty_estimates(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_estimates'], 0)

    def test_dashboard_empty_jobs(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_jobs'], 0)

    def test_dashboard_empty_invoices(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_invoices'], 0)

    def test_dashboard_zero_revenue_when_empty(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['paid_revenue'], Decimal('0.00'))
        self.assertEqual(
            response.context['outstanding_revenue'], Decimal('0.00'))


class DashboardStatisticsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            name="Stats Customer",
            email="stats@example.com"
        )

    def test_estimate_conversion_tracking(self):
        # Create 10 estimates: 5 pending, 5 accepted
        for i in range(5):
            Estimate.objects.create(
                customer=self.customer,
                description=f"Pending estimate {i}",
                estimated_cost=Decimal('1000.00'),
                visit_date=date(2024, 12, 1),
                status='pending'
            )
        for i in range(5):
            estimate = Estimate.objects.create(
                customer=self.customer,
                description=f"Accepted estimate {i}",
                estimated_cost=Decimal('1000.00'),
                visit_date=date(2024, 12, 1),
                status='accepted'
            )
            Job.objects.create(
                estimate=estimate,
                start_date=date(2024, 12, 1),
                status='scheduled'
            )

        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_estimates'], 10)
        self.assertEqual(response.context['accepted_estimates'], 5)

    def test_job_completion_rate(self):
        # Create 10 jobs: 3 completed, 4 ongoing, 3 scheduled
        for i in range(10):
            estimate = Estimate.objects.create(
                customer=self.customer,
                description=f"Job estimate {i}",
                estimated_cost=Decimal('1000.00'),
                visit_date=date(2024, 12, 1),
                status='accepted'
            )

            if i < 3:
                status = 'completed'
                end_date = date(2024, 12, 5)
            elif i < 7:
                status = 'ongoing'
                end_date = None
            else:
                status = 'scheduled'
                end_date = None

            Job.objects.create(
                estimate=estimate,
                start_date=date(2024, 12, 1),
                end_date=end_date,
                status=status
            )

        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_jobs'], 10)
        self.assertEqual(response.context['completed_jobs'], 3)

    def test_revenue_calculation(self):
        # Create 5 invoices: 3 paid, 2 unpaid
        for i in range(5):
            estimate = Estimate.objects.create(
                customer=self.customer,
                description=f"Revenue estimate {i}",
                estimated_cost=Decimal(f'{1000 + i * 100}.00'),
                visit_date=date(2024, 12, 1),
                status='accepted'
            )
            job = Job.objects.create(
                estimate=estimate,
                start_date=date(2024, 12, 1),
                status='completed'
            )

            paid = i < 3
            Invoice.objects.create(
                job=job,
                total_amount=Decimal(f'{1000 + i * 100}.00'),
                due_date=date(2025, 1, 1),
                paid=paid
            )

        # Expected paid revenue: 1000 + 1100 + 1200 = 3300
        # Expected unpaid revenue: 1300 + 1400 = 2700
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.context['total_invoices'], 5)
        self.assertEqual(response.context['paid_invoices'], 3)
        self.assertEqual(response.context['paid_revenue'], Decimal('3300.00'))
        self.assertEqual(
            response.context['outstanding_revenue'], Decimal('2700.00'))
