from django.urls import path
from .views import CustomerListView, CustomerCreateView

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),
    path('create/', CustomerCreateView.as_view(), name='customer-create'),
]
