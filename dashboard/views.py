from jobs.models import Job
from invoices.models import Invoice
from estimates.models import Estimate
from customer.models import Customer
from django.shortcuts import render
from django.db.models import Sum
import matplotlib.pyplot as plt
import base64
import io
from decimal import Decimal

import matplotlib
matplotlib.use('Agg')


def _figure_to_base64(figure):
    """Convert a matplotlib figure to a base64 PNG string for inline rendering."""
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(figure)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def _build_revenue_chart():
    paid_invoices = Invoice.objects.filter(paid=True).order_by('issued_date')
    labels = [invoice.issued_date.strftime(
        '%d %b') for invoice in paid_invoices]
    values = [float(invoice.total_amount) for invoice in paid_invoices]

    if not values:
        labels = ['No Revenue Yet']
        values = [0]

    figure, axis = plt.subplots(figsize=(8, 3.6))
    axis.plot(labels, values, marker='o', color='#1f77b4', linewidth=2)
    axis.set_title('Paid Revenue Trend')
    axis.set_xlabel('Issued Date')
    axis.set_ylabel('Amount (KES)')
    axis.grid(alpha=0.3)
    axis.tick_params(axis='x', rotation=30)
    figure.tight_layout()
    return _figure_to_base64(figure)


def _build_job_status_chart():
    status_rows = Job.objects.values('status')
    status_counts = {
        'scheduled': 0,
        'ongoing': 0,
        'completed': 0,
    }
    for row in status_rows:
        status_counts[row['status']] = status_counts.get(row['status'], 0) + 1

    labels = ['Scheduled', 'Ongoing', 'Completed']
    values = [status_counts['scheduled'],
              status_counts['ongoing'], status_counts['completed']]

    if sum(values) == 0:
        labels = ['No Jobs Yet']
        values = [1]
        colors = ['#d9d9d9']
    else:
        colors = ['#ffd166', '#ef476f', '#06d6a0']

    figure, axis = plt.subplots(figsize=(5.5, 4))
    axis.pie(values, labels=labels, autopct='%1.0f%%',
             colors=colors, startangle=90)
    axis.set_title('Job Status Distribution')
    axis.axis('equal')
    figure.tight_layout()
    return _figure_to_base64(figure)


def dashboard_home(request):
    total_customers = Customer.objects.count()
    total_estimates = Estimate.objects.count()
    accepted_estimates = Estimate.objects.filter(status='accepted').count()
    total_jobs = Job.objects.count()
    completed_jobs = Job.objects.filter(status='completed').count()
    total_invoices = Invoice.objects.count()
    paid_invoices = Invoice.objects.filter(paid=True).count()

    paid_revenue = Invoice.objects.filter(paid=True).aggregate(
        total=Sum('total_amount'))['total'] or Decimal('0.00')
    outstanding_revenue = Invoice.objects.filter(paid=False).aggregate(
        total=Sum('total_amount'))['total'] or Decimal('0.00')

    context = {
        'total_customers': total_customers,
        'total_estimates': total_estimates,
        'accepted_estimates': accepted_estimates,
        'total_jobs': total_jobs,
        'completed_jobs': completed_jobs,
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'paid_revenue': paid_revenue,
        'outstanding_revenue': outstanding_revenue,
        'revenue_chart': _build_revenue_chart(),
        'job_status_chart': _build_job_status_chart(),
    }
    return render(request, 'dashboard/home.html', context)
