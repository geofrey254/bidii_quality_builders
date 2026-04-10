from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Estimate
from .services import accept_estimate


class EstimateListView(ListView):
    model = Estimate
    template_name = 'estimates/list.html'
    context_object_name = 'estimates'


class EstimateCreateView(CreateView):
    model = Estimate
    fields = ['customer', 'description', 'visit_date', 'estimated_cost']
    template_name = 'estimates/estimate_form.html'
    success_url = reverse_lazy('estimate-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        input_class = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-150'
        form.fields['customer'].widget.attrs.update({'class': input_class})
        form.fields['description'].widget.attrs.update(
            {'class': input_class, 'rows': 4})
        form.fields['visit_date'].widget.attrs.update({'class': input_class})
        form.fields['estimated_cost'].widget.attrs.update(
            {'class': input_class})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f'Estimate created for {self.object.customer.name}')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


def accept_estimate_view(request, pk):
    if request.method != 'POST':
        return redirect('estimate-list')

    estimate = get_object_or_404(Estimate, pk=pk)
    if estimate.status != 'pending':
        messages.warning(request, 'This estimate cannot be accepted.')
        return redirect('estimate-list')

    accept_estimate(estimate)
    messages.success(
        request, f'Estimate for {estimate.customer.name} accepted. Job created.')
    return redirect('estimate-list')
