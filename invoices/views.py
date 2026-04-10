from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from decimal import Decimal
from .models import Invoice
from jobs.models import Job


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/list.html'
    context_object_name = 'invoices'


class InvoiceCreateView(CreateView):
    model = Invoice
    fields = ['job', 'total_amount']
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoice-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        input_class = 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-150'
        form.fields['job'].queryset = Job.objects.filter(
            status='completed',
            invoice__isnull=True,
        )
        form.fields['job'].empty_label = 'Select a completed job'
        form.fields['job'].widget.attrs.update({'class': input_class})
        form.fields['total_amount'].widget.attrs.update({'class': input_class})
        return form

    def form_valid(self, form):
        total_amount = form.cleaned_data.get('total_amount')
        if not total_amount or total_amount <= Decimal('0'):
            messages.error(
                self.request, 'Invoice amount must be greater than zero.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        messages.success(self.request, 'Invoice created successfully.')
        return response

    def form_invalid(self, form):
        if not form.errors.get('non_field_errors'):
            messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


def mark_invoice_paid(request, pk):
    if request.method != 'POST':
        return redirect('invoice-list')

    invoice = get_object_or_404(Invoice, pk=pk)
    if invoice.paid:
        messages.warning(request, 'This invoice is already marked as paid.')
        return redirect('invoice-list')

    invoice.paid = True
    invoice.save(update_fields=['paid'])
    messages.success(
        request, f'Invoice marked as paid (Amount: KES {invoice.total_amount})')
    return redirect('invoice-list')
