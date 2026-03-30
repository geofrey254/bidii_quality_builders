from django.views.generic import ListView, CreateView
from .models import Customer
from django.urls import reverse_lazy


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/list.html'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'phone_number', 'email', 'address']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')
