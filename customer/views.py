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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        input_class = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-150'
        form.fields['name'].widget.attrs.update({'class': input_class})
        form.fields['phone_number'].widget.attrs.update({'class': input_class})
        form.fields['email'].widget.attrs.update({'class': input_class})
        form.fields['address'].widget.attrs.update(
            {'class': input_class, 'rows': 4})
        return form
