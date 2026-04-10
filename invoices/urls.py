from django.urls import path
from .views import InvoiceListView, InvoiceCreateView, mark_invoice_paid


urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list'),
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('<int:pk>/mark-paid/', mark_invoice_paid, name='invoice-mark-paid'),
]
