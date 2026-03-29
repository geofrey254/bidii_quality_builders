from django.views.generic import ListView, CreateView
from .models import Customer
from django.urls import reverse_lazy


class CustomerListView(ListView):
    model = Customer
    template_name = '/templates/customers/list.html'


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['name', 'phone', 'email', 'address']
    success_url = reverse_lazy('customer-list')
